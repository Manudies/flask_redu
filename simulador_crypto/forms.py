from flask_wtf import FlaskForm
from wtforms import DecimalField, HiddenField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo


class MovimientoForm(FlaskForm):
    id = HiddenField()
    fecha = HiddenField()
    hora = HiddenField()
    moneda_from = SelectField('Moneda de origen', choices=[
                              'EUR', 'BTC', 'ETH', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB'], validators=[DataRequired(message='Tienes que elegir una moneda')])

    cantidad_from = DecimalField('Cantidad de origen', validators=[
                                 DataRequired(message='No puede haber un movimiento sin cantidad de origen')])

    moneda_to = SelectField('Moneda de destino', choices=[
                            'EUR', 'BTC', 'ETH', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB'])

    calcular = SubmitField('Calcular')
    validar = SubmitField('Validar')
