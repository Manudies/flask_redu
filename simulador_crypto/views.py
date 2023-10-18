from flask import render_template
from . import app


@app.route("/")
def inicio():
    return render_template('inicio.html', active_route='inicio')


@app.route("/purchase")
def compra():
    return render_template('compra.html', active_route='compra')


@app.route("/status")
def estado():
    return render_template('estado.html', active_route='estado')
