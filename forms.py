from flask_wtf import FlaskForm
from wtfforms import StringField

class RegistrationFiels(FlaskForm):
	username = StringField('Username')