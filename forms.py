from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
	username = StringField('Username', 
				validators=[DataRequired(), Length(min=3, max=30)])
	email = StringField('Email', 
				validators=[DataRequired(), Email()])
	password = PasswordField('Password', 
				validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password',
				validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	username = StringField('Username', 
				validators=[DataRequired(), Length(min=3, max=30)])
	password = PasswordField('Password', 
				validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
	picture = FileField('Profile image', validators=[])
	name = StringField('Name', validators=[DataRequired(), Length(max=30)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
	age = IntegerField('Age', validators=[NumberRange(min=5, max=100)])
	#gender = SelectField('Gender', default=18, choices=['Male', 'Female'])
	submit = SubmitField('Apply')
