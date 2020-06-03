from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectMultipleField, PasswordField, SubmitField, BooleanField, \
					FileField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from libs.User import User
from libs.Group import Group
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


class EditProfileForm(FlaskForm):
	picture = FileField('Profile image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	name = StringField('Name', validators=[DataRequired(), Length(max=30)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
	age = IntegerField('Age', validators=[])
	gender_choices = [('Male', 'Male'), ('Female', 'Female')]  # (value, label)
	gender = SelectField('Gender', choices=gender_choices)
	sport_choices = Sports.get_choices()
	# TODO add defaults for sport
	sport = SelectMultipleFields('Sport', choices=sport_choices)
	submit = SubmitField('Update')

	def validate_age(self, age):
		if age.data < 10 or age.data > 100:
			raise ValidationError('Invalid age!')


class NewGroupFrom(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
	sport = SelectField('Sport', choices=Sports.get_choices(), validators=[DataRequired()])
	submit = SubmitField('Create')

	def validate_name(self, name):
		group = Group.query.filter_by(name=name.data).first()
		print(group)
		if group:
			raise ValidationError('Name already taken!')


class SearchGroupForm(FlaskForm):
	name = StringField('Name', validators=[Length(max=50)])
	choices = Sports.get_choices()
	choices.append(("None", "None"))
	sport = SelectField('Sport', choices=choices, default="None")

	submit = SubmitField('Search')


class NewEventForm(FlaskForm):
	name = StringField('Name', validators=[Length(max=100), DataRequired()])
	description = TextAreaField('Description', validators=[Length(max=300)])
	sport_choices = Sports.get_choices()
	sport = SelectField('Sport', choices=sport_choices, default="Tennis")
	assigned_group = SelectField('Group')
	# date = DateField("Date")
	# time = TimeField("Time")
	time = DateTimeLocalField("Time", format='%Y-%m-%dT%H:%M')
	submit = SubmitField('Create')

	def __init__(self, groups, *args, **kwargs):
		super().__init__(*args, **kwargs)
		group_choices = [(str(i.id), i.name) for i in groups]
		group_choices.append(("None", "None"))
		self.assigned_group.choices = group_choices



