from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    url = StringField('url', validators=[DataRequired()])
    remember_me = BooleanField('Muista minut', default=False)