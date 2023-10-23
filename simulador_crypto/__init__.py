import os

from flask import Flask

RUTA = os.path.join('simulador_crypto', 'data', 'crypto.db')
app = Flask(__name__)
app.config.from_prefixed_env()
