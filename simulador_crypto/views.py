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
        return render_template('compra.html', form=formulario, active_route='compra')
    if request.method == 'POST':
        formulario = MovimientoForm(data=request.form)
        if formulario.calcular.data:
            # Llamar a la API
            rate = consultar_cambio(
                formulario.moneda_from.data, formulario.moneda_to.data)
            formulario.precio_unitario.process_data(rate)
            q_to = float(formulario.precio_unitario.data) * \
                float(formulario.cantidad_from.data)
            formulario.cantidad_to.process_data(q_to)
            # formulario.cantidad_to = formulario.cantidad_from.data*formulario.precio_unitario
            # print(cantidad_to)
            # print(rate)
            return render_template('compra.html', form=formulario, active_route='compra')
        else:
            # Guardo en la base de datos
            print('Guardar en la BD')
            print(formulario.precio_unitario)
            db = DBManager(RUTA)
            parametros = (
                formulario.moneda_from.data,
                float(formulario.cantidad_from.data),
                formulario.moneda_to.data,
                float(formulario.cantidad_to.data)
            )
            # consulta = f'INSERT INTO movimientos (fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES ({datetime("now")}, {datetime("localtime")}, {formulario.moneda_from.data}, {formulario.cantidad_from.data}, {formulario.moneda_to.data}, {formulario.cantidad_to.data})'
            consulta2 = "INSERT INTO movimientos (fecha, hora, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (date('now'), time('now', 'localtime'),?,?,?,?)"
            db.consultaConParametros(consulta2, parametros)
            return render_template('compra.html', form=formulario, active_route='compra')


@app.route("/status")
def estado():
    return render_template('estado.html', active_route='estado')
