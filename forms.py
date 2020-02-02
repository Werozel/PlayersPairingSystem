from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import Field, RadioField, StringField, SelectMultipleField, PasswordField, SubmitField, BooleanField, FileField, IntegerField, SelectField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from libs.User import User
from constants.constants import Sports


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


class SelectMultipleFields(SelectMultipleField):

	def pre_validate(self, form):
		pass

	def process_formdata(self, valuelist):
		self.data = valuelist

class SportField(SelectMultipleField):
	name = ListWidget(prefix_label=False)
	check = CheckboxInput()

class EditProfileForm(FlaskForm):
	picture = FileField('Profile image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	name = StringField('Name', validators=[DataRequired(), Length(max=30)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
	age = IntegerField('Age', validators=[])
	gender_choices = [('Male', 'Male'), ('Female', 'Female')]  # (value, label)
	gender = SelectField('Gender', choices=gender_choices)
	sport_choices = [(i, i) for i in Sports.get_list()]
	sport = SelectMultipleFields('Sport', choices=sport_choices)
	submit = SubmitField('Update')

	def validate_age(self, age):
		if age.data < 10 or age.data > 100:
			raise ValidationError('Invalid age!')

