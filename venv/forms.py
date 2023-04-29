from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class HeaderForm(FlaskForm):
    round = IntegerField('Round')
    lookback = IntegerField('Look Back Rounds')
    isGetData = BooleanField('Update Data from FPL Site')
    submit = SubmitField('Submit')

