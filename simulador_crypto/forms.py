from flask_wtf import FlaskForm
from wtforms import DecimalField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms_validators import NotEqualTo


class MovimientoForm(FlaskForm):
    monedas = ('EUR', 'ADA', 'BTC', 'DOGE', 'DOT', 'ETH',
               'SHIB', 'SOL', 'USDT', 'XRP')

    def not_equal_to(self, campo):
        self.campo = campo
        if self.campo == self.data:
            raise ValidationError("Las monedas no pueden ser iguales")

    id = HiddenField()
    fecha = HiddenField()
    hora = HiddenField()
    moneda_from = SelectField('Moneda de origen', choices=monedas,
                              validators=[DataRequired(message='Tienes que elegir una moneda')
                                          ])

    cantidad_from = DecimalField('Cantidad de origen',
                                 validators=[DataRequired(message='No puede haber un movimiento sin cantidad de origen')])

    moneda_to = SelectField('Moneda de destino', choices=monedas,
                            validators=[DataRequired(message='No puede haber un movimiento sin cantidad'),
                                        NotEqualTo("moneda_from", message="Las monedas no pueden ser iguales")])

    calcular = SubmitField('Calcular')
    validar = SubmitField('Validar')
