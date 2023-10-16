from flask import render_template
from . import app


@app.route("/")
def inicio():
    return render_template('inicio.html')


@app.route("/purchase")
def compra():
    return render_template('compra.html')


@app.route("/status")
def estado():
    return render_template('estado.html')
