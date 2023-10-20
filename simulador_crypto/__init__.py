import os

from flask import Flask

RUTA = os.path.join('simulador_crypto', 'data', 'crypto.db')
app = Flask(__name__)
