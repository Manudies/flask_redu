from .api_rate import consultar_cambio
import datetime
from .models import DBManager
from flask import flash, redirect, render_template, request, url_for
from . import app, RUTA
from .forms import MovimientoForm


@app.route("/")
def inicio():
    # Crear la base de datos y la tabla
    db = DBManager(RUTA)
    try:
        print("Intento el try")
        sql_leer = 'SELECT id, fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to FROM movimientos'
        movimientos = db.consultaSQL(sql_leer)
        print("Lo he conseguido")
    except:
        archivo = ValueError
        if archivo:
            print("No he conseguido el try por que no hay base de datos")
            sql_crear = 'CREATE TABLE "movimientos" ("id"	INTEGER NOT NULL UNIQUE,"fecha"	TEXT NOT NULL,"hora" TEXT NOT NULL,"moneda_from" TEXT NOT NULL,"cantidad_from" NUMERIC NOT NULL,"moneda_to" TEXT NOT NULL,"cantidad_to" NUMERIC NOT NULL DEFAULT 0, PRIMARY KEY("id" AUTOINCREMENT))'
            db.crearSQL(sql_crear)
            movimientos = db.consultaSQL(sql_leer)
            print("Base de datos creada")
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
                print(he_vendido_crypto[0]["IFNULL(sum(cantidad_from), 0)"])
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
                # db = DBManager(RUTA)
                # consulta = 'SELECT moneda_to FROM movimientos'
                # hay_cryptos = db.consultaSQL(consulta)
                # print(hay_cryptos)
                # if hay_cryptos:
                rate = consultar_cambio(
                    formulario.moneda_from.data, formulario.moneda_to.data)
                qto = float(rate) * \
                    float(formulario.cantidad_from.data)
                return render_template('compra.html', form=formulario, data=[rate, qto, formulario.moneda_to.data, formulario.moneda_from.data], active_route='compra')
            else:
                # Pulsar boton validad. Guardo en la base de datos
                rate = consultar_cambio(
                    formulario.moneda_from.data, formulario.moneda_to.data)
                qto = float(rate) * \
                    float(formulario.cantidad_from.data)
                print('Guardar en la BD')
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
            print("voy por errores")
            errores = []
            for key in formulario.errors:
                errores.append((key, formulario.errors[key]))
                rate = ""
                qto = ""
            return render_template('compra.html', form=formulario, data=[rate, qto, formulario.moneda_to.data, formulario.moneda_from.data], active_route='compra', errors=errores)


@app.route("/status")
def estado():
    return render_template('estado.html', active_route='estado')
