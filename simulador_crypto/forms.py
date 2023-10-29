from flask_wtf import FlaskForm
from wtforms import DecimalField, HiddenField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange


class MovimientoForm(FlaskForm):
    id = HiddenField()
    fecha = HiddenField()
    hora = HiddenField()
    moneda_from = SelectField('Moneda de origen', choices=[
                              'EUR', 'BTC', 'ETH', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB'])

    cantidad_from = DecimalField('Cantidad de origen', validators=[
                                 DataRequired(message='No puede haber un movimiento sin cantidad')])

    moneda_to = SelectField('Moneda de destino', choices=[
        'EUR', 'BTC', 'ETH', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB'])

    precio_unitario = FloatField('Precio Unitario:')

    cantidad_to = FloatField('Cantidad de destino:')
    calcular = SubmitField('Calcular')
    validar = SubmitField('Validar')
