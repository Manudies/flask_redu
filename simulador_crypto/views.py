from . import app


@app.route("/")
def home():
    return "Prueba de servidor"
