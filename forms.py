from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from libs.User import User


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

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is already taken')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Account with this email already exists')


class LoginForm(FlaskForm):
	username = StringField('Username', 
				validators=[DataRequired(), Length(min=3, max=30)])
	password = PasswordField('Password', 
				validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
	picture = FileField('Profile image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	name = StringField('Name', validators=[DataRequired(), Length(max=30)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
	age = IntegerField('Age', validators=[])
	gender_choices = [('Male', 'Male'), ('Female', 'Female')]  # (value, label)
	gender = SelectField('Gender', default=18, choices=gender_choices)
	submit = SubmitField('Update')

	def validate_age(self, age):
		if 10 > age.data > 100:
			raise ValidationError('')

