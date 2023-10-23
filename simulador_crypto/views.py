from .models import DBManager
from flask import render_template, request
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
            sql_crear = 'CREATE TABLE "movimientos" ("id"	INTEGER NOT NULL UNIQUE,"fecha"	TEXT NOT NULL,"hora" TEXT NOT NULL,"moneda_from" TEXT NOT NULL,"cantidad_from" NUMERIC NOT NULL,"moneda_to" TEXT NOT NULL,"precio_unitario"	INTEGER NOT NULL,"cantidad_to" NUMERIC NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))'
            db.crearSQL(sql_crear)
            movimientos = db.consultaSQL(sql_leer)
            print("Base de datos creada")
    return render_template('inicio.html', active_route='inicio', movs=movimientos)


@app.route("/purchase")
def compra():
    formulario = MovimientoForm()
    return render_template('compra.html', form=formulario, active_route='compra')


@app.route("/status")
def estado():
    return render_template('estado.html', active_route='estado')
