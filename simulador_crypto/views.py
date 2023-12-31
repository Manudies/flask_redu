from .api_rate import consultar_cambio, consultar_inversion
import locale
from .models import DBManager
from flask import flash, redirect, render_template, request, url_for
from . import app, RUTA
from .forms import MovimientoForm

locale.setlocale(category=locale.LC_ALL, locale="es_ES")


@app.route("/")
def inicio():
    # Crear la base de datos y la tabla
    db = DBManager(RUTA)
    try:
        sql_leer = 'SELECT id, fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to FROM movimientos'
        movimientos = db.consultaSQL(sql_leer)
    except:
        archivo = ValueError
        if archivo:
            sql_crear = 'CREATE TABLE "movimientos" ("id"	INTEGER NOT NULL UNIQUE,"fecha"	TEXT NOT NULL,"hora" TEXT NOT NULL,"moneda_from" TEXT NOT NULL,"cantidad_from" NUMERIC NOT NULL,"moneda_to" TEXT NOT NULL,"cantidad_to" NUMERIC NOT NULL DEFAULT 0, PRIMARY KEY("id" AUTOINCREMENT))'
            db.crearSQL(sql_crear)
            movimientos = db.consultaSQL(sql_leer)
    return render_template('inicio.html', active_route='inicio', movs=movimientos)


@app.route('/purchase', methods=['GET', 'POST'])
def compra():
    if request.method == 'GET':
        formulario = MovimientoForm()
        rate = ""
        qto = ""
        return render_template('compra.html', form=formulario, data=[rate, qto, formulario.moneda_to.data, formulario.moneda_from.data], active_route='compra')
    if request.method == 'POST':
        formulario = MovimientoForm(data=request.form)
        if formulario.validate():
            if formulario.moneda_from.data != "EUR":
                # Compruebo si tengo esa cripto moneda en el monedero y si la tengo obtengo el total
                db = DBManager(RUTA)
                consulta = "SELECT IFNULL(sum(cantidad_to), 0) FROM movimientos WHERE moneda_to == ?"
                consulta2 = "SELECT IFNULL(sum(cantidad_from), 0) FROM movimientos WHERE moneda_from == ?"
                moneda = (formulario.moneda_from.data,)
                he_comprado_crypto = db.consultaCrypto(consulta, moneda)
                he_vendido_crypto = db.consultaCrypto(consulta2, moneda)
                valor_moneda = (he_comprado_crypto[0]["IFNULL(sum(cantidad_to), 0)"] -
                                he_vendido_crypto[0]["IFNULL(sum(cantidad_from), 0)"])
                # Si no tengo moneda o no tengo suficiente devuelvo un error.
                if valor_moneda <= formulario.cantidad_from.data or valor_moneda == 0:
                    errores = []
                    error = ('', [
                             (f"No tienes suficientes monedas. Tienes: {valor_moneda} {formulario.moneda_from.data}'s")])
                    errores.append(error)
                    return render_template('compra.html', form=formulario, data=[formulario.moneda_to.data, formulario.moneda_from.data], active_route='compra', errors=errores)
            # Calculo el precio de cambio
            if formulario.calcular.data:
                rate = consultar_cambio(
                    formulario.moneda_from.data, formulario.moneda_to.data)
                qto = float(rate) * \
                    float(formulario.cantidad_from.data)
                return render_template('compra.html', form=formulario, data=[rate, qto, formulario.moneda_to.data, formulario.moneda_from.data], active_route='compra')
                # Si no es calcular es Validar . Guardo en la base de datos
            else:
                rate = consultar_cambio(
                    formulario.moneda_from.data, formulario.moneda_to.data)
                qto = float(rate) * \
                    float(formulario.cantidad_from.data)
                db = DBManager(RUTA)
                parametros = (
                    formulario.moneda_from.data,
                    float(formulario.cantidad_from.data),
                    formulario.moneda_to.data,
                    round(qto, 10)
                )
                consulta = "INSERT INTO movimientos (fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (date('now'), time('now', 'localtime'),?,?,?,?)"
                resultado = db.consultaConParametros(
                    consulta, parametros)
                if resultado:
                    flash(
                        "El moviento se ha guardado en tu monedero de Cryptos", category="exito")
                    return redirect(url_for('inicio'))
                return "No se ha podido realizar la transacción. Intentelo en unos instantes"

        else:
            errores = []
            for key in formulario.errors:
                errores.append((key, formulario.errors[key]))
                rate = ""
                qto = ""
            return render_template('compra.html', form=formulario, data=[rate, qto, formulario.moneda_to.data, formulario.moneda_from.data], active_route='compra', errors=errores)


@app.route("/status")
def estado():
    # Obtenemos el total de euros invertidos y recuperados.
    db = DBManager(RUTA)
    consulta = "SELECT IFNULL(sum(cantidad_from), 0) as cantidad_from_EUR FROM movimientos WHERE moneda_from == 'EUR'"
    consulta2 = "SELECT IFNULL(sum(cantidad_to), 0) as cantidad_to_EUR FROM movimientos WHERE moneda_to == 'EUR'"
    eur_inver = db.consultaSQL(consulta)
    eur_recup = db.consultaSQL(consulta2)

    total_eur_inver = eur_inver[0]["cantidad_from_EUR"]
    saldo_euros_inver = (eur_recup[0]["cantidad_to_EUR"]) - \
        (eur_inver[0]["cantidad_from_EUR"])

    # Obtengo la suma de cada cripto comprada o vendida en dos listas.
    # Los parametros deben coincidir en número y cantidad con parámetro monedas de form.py. El EUR no se incluye
    consulta3 = "SELECT IFNULL(sum(cantidad_from), 0) as cantidad_from FROM movimientos WHERE moneda_from == ?"
    consulta4 = "SELECT IFNULL(sum(cantidad_to), 0) as cantidad_to FROM movimientos WHERE moneda_to == ?"
    parametros = [('ADA',), ('BTC',), ('DOGE',), ('DOT',),
                  ('ETH',), ('SHIB',), ('SOL',), ('USDT',), ('XRP',)]
    venta_crypto = []
    compra_crypto = []
    m = 0
    for i in parametros:
        crypto_ven = db.consultaCrypto(consulta3, parametros[m])
        crypto_com = db.consultaCrypto(consulta4, parametros[m])
        venta_crypto.append(crypto_ven)
        compra_crypto.append(crypto_com)
        m += 1
    # Agrego a una lista los valores ordenados
    venta_crypto_data = []
    compra_crypto_data = []
    for i in compra_crypto:
        venta_crypto_data.append(i[0]["cantidad_to"])
    for i in venta_crypto:
        compra_crypto_data.append(i[0]["cantidad_from"])

    # Resto las monedas compradas y vendidas
    resta_crypto = list(
        map(lambda x, y: x-y, venta_crypto_data, compra_crypto_data))

    # Llamo a la API y consulto el valor de cambio de cada moneda y lo guardo en una lista
    cambio_monedas = consultar_inversion()

    # Divido las listas
    multi_crypto = list(
        map(lambda x, y: x/y, resta_crypto, cambio_monedas))

    valor_euros_cryptos = sum(multi_crypto)

    valor_actual = total_eur_inver + saldo_euros_inver + valor_euros_cryptos
    ganancia = valor_actual-total_eur_inver
    ganancia = locale.currency(ganancia, symbol=True, grouping=True)
    valor_actual = locale.currency(valor_actual, symbol=True, grouping=True)
    total_eur_inver = locale.currency(
        total_eur_inver, symbol=True, grouping=True)

    return render_template('estado.html', data=[total_eur_inver, valor_actual, ganancia], active_route='estado')
