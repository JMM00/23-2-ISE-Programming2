from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class HistoryForm(FlaskForm):
    rent_date = DateTimeField('Rent Date', validators=[DataRequired()])
    rent_station = StringField('Rent Station', validators=[DataRequired()])
    rent_time = DateTimeField('Rent Time', validators=[DataRequired()])
    return_time = DateTimeField('Return Time', validators=[DataRequired()])
    distance = FloatField('Distance', validators=[DataRequired()])