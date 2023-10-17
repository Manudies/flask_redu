from flask import render_template
from . import app


@app.route("/")
def inicio():
    ruta = "http://127.0.0.1:5000/"
    return render_template('inicio.html', actual_inicio=ruta)


@app.route("/purchase")
def compra():
    ruta = "http://127.0.0.1:5000/purchase"
    return render_template('compra.html', actual_compra=ruta)


@app.route("/status")
def estado():
    ruta = "http://127.0.0.1:5000/status"
    return render_template('estado.html', actual_estado=ruta)
