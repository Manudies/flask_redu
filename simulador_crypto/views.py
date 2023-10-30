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
            sql_crear = 'CREATE TABLE "movimientos" ("id"	INTEGER NOT NULL UNIQUE,"fecha"	TEXT NOT NULL,"hora" TEXT NOT NULL,"moneda_from" TEXT NOT NULL,"cantidad_from" NUMERIC NOT NULL,"moneda_to" TEXT NOT NULL,"cantidad_to" NUMERIC NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))'
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
            if formulario.moneda_from != "EUR":
                # Compruebo si tengo esa cripto moneda en el monedero y si la tengo obtengo el total
                db = DBManager(RUTA)
                consulta = "SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to == ?"
                parametro = (formulario.moneda_from.data,)
                hay_cryptos = db.consultaCrypto(consulta, parametro)
                print(hay_cryptos)
                for i in hay_cryptos:
                    dic = i
                    valor = dic["sum(cantidad_to)"]
                if valor <= formulario.cantidad_from.data:
                    print('No tienes suficientes monedas')
                else:
                    print("Puedes realizar la operacion")
            if formulario.calcular.data:
                db = DBManager(RUTA)
                consulta = 'SELECT moneda_to FROM movimientos'
                hay_cryptos = db.consultaSQL(consulta)
                if hay_cryptos:
                    rate = consultar_cambio(
                        formulario.moneda_from.data, formulario.moneda_to.data)
                    qto = float(rate) * \
                        float(formulario.cantidad_from.data)
                    return render_template('compra.html', form=formulario, data=[rate, qto, formulario.moneda_to.data, formulario.moneda_from.data], active_route='compra')
            else:
                # Guardo en la base de datos
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
                return "No se ha podido realizar la transacción"
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
