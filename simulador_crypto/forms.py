from flask_wtf import FlaskForm
from wtforms import (DecimalField, HiddenField, SubmitField, SelectField)
from wtforms.validators import DataRequired, NumberRange


class MovimientoForm(FlaskForm):
    id = HiddenField()
    fecha = HiddenField()
    hora = HiddenField()
    moneda_from = SelectField('Moneda de origen', choices=[
                              'EUR', 'BTC', 'ETH', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB'])

    cantidad_from = DecimalField('Cantidad de origen', places=10, validators=[
        DataRequired(message='No puede haber un movimiento sin cantidad'),
        NumberRange(min=0.0000000001, message='no valido')])

    moneda_to = SelectField('Moneda de destino', choices=[
        'EUR', 'BTC', 'ETH', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB'])

    precio_unitario = DecimalField('Precio Unitario', places=10, validators=[
        DataRequired(message='No puede haber un movimiento sin cantidad'),
        NumberRange(min=0.0000000001, message='no valido')])

    cantidad_to = DecimalField('Cantidad de destino')
    calcular = SubmitField('Calcular')
    validar = SubmitField('Validar')
