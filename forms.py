from typing import List

from src.youtube_links import is_youtube_link
from wtforms import Form
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SelectMultipleField, PasswordField, SubmitField, BooleanField, HiddenField, \
					FileField, IntegerField, SelectField, TextAreaField, FieldList, TimeField, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from flask_babel import gettext
from libs.models.PlayTimes import PlayTimes
from libs.models.User import User
from libs.models.Group import Group
from libs.models.Event import Event
from constants.constants import Sports, DayOfWeek

import re


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password', validators=[DataRequired()])

	submit = SubmitField('Sign Up')

	@staticmethod
	def validate_username(_, username):
		if not re.match("^[A-Za-z0-9_-]*$", username.data):
			raise ValidationError(gettext('Username can only contain letters, numbers, underscores and dashes'))
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError(gettext('This username is already taken'))

	@staticmethod
	def validate_email(_, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError(gettext('Account with this email already exists'))

	@staticmethod
	def validate_confirm_password(form, confirm_password):
		if not form.password.data == confirm_password.data:
			raise ValidationError(gettext("Passwords doesn't match!"))


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class SelectMultipleFields(SelectMultipleField):

	def pre_validate(self, form):
		pass

	def process_formdata(self, value_list):
		self.data = value_list


# class PlayTimeForm(FlaskForm):
# 	play_time_id = IntegerField('Play time id')
# 	day_of_week = SelectField('Day of week', choices=DayOfWeek.days_of_week)
# 	start_time = TimeField('Start time')
# 	end_time = TimeField('End time')
#
# 	@staticmethod
# 	def validate_end_time(form, end_time):
# 		if form.start_time.data is not None and \
# 			form.start_time.data >= end_time.data:
# 			raise ValidationError(gettext("Start time can't be after end time"))

	# def __init_self, *args, **kwargs):
	# 	super().__init_*args, **kwargs)
	# 	self.id.data = kwargs.get('id')


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
	# times = FieldList(FormField(PlayTimeForm), max_entries=7)
	submit = SubmitField('Update')

	@staticmethod
	def validate_age(_, age):
		if age.data < 10 or age.data > 100:
			raise ValidationError(gettext('Invalid age!'))

	def __init__(self, times_values: List[PlayTimes] = None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# if times_values is not None and len(times_values) > 0:
		# 	for time in times_values:
		# 		self.times.append_entry({
		# 			'play_time_id': time.id,
		# 			'day_of_week': time.day_of_week,
		# 			'start_time': time.start_time,
		# 			'end_time': time.end_time
		# 		})
		# self.times.append_entry()


class NewGroupFrom(FlaskForm):
	closed = BooleanField('Closed')
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
	sport = SelectField('Sport', choices=Sports.get_choices(), validators=[DataRequired()])
	submit = SubmitField('Submit')

	@staticmethod
	def validate_name(form, name):
		group = Group.query.filter_by(name=name.data).first()
		current_group_id = -1 if form.current_group is None else form.current_group.id
		if group and group.id != current_group_id:
			raise ValidationError(gettext('Name already taken!'))

	def __init__(self, current_group=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.current_group = current_group


class SearchGroupForm(FlaskForm):
	name = StringField('Name', validators=[Length(max=50)])
	choices = Sports.get_choices()
	choices.append(("None", "None"))
	sport = SelectField('Sport', choices=choices, default="None")

	submit = SubmitField('Search')


class NewEventForm(FlaskForm):
	closed = BooleanField('Closed')
	name = StringField('Name', validators=[Length(max=100), DataRequired()])
	description = TextAreaField('Description', validators=[Length(max=300)])
	sport_choices = Sports.get_choices()
	sport = SelectField('Sport', choices=sport_choices, default="Tennis")
	assigned_group = SelectField('Group')
	# date = DateField("Date")
	# time = TimeField("Time")
	time = DateTimeLocalField("Time", format='%Y-%m-%dT%H:%M')
	submit = SubmitField('Create')

	@staticmethod
	def validate_name(_, name):
		events = Event.query.filter_by(name=name.data).first()
		if events:
			raise ValidationError(gettext("Name already taken!"))

	def __init__(self, groups, *args, **kwargs):
		super().__init__(*args, **kwargs)
		group_choices = [(str(i.id), i.name) for i in groups]
		group_choices.append(("None", "None"))
		self.assigned_group.choices = group_choices


class EditEventForm(FlaskForm):
	closed = BooleanField('Closed')
	name = StringField('Name', validators=[Length(max=100), DataRequired()])
	description = TextAreaField('Description', validators=[Length(max=300)])
	sport_choices = Sports.get_choices()
	sport = SelectField('Sport', choices=sport_choices, default="Tennis")
	time = DateTimeLocalField('Time', format='%Y-%m-%dT%H:%M')
	submit = SubmitField('Update')

	@staticmethod
	def validate_name(form, name):
		current_event_id = -1 if form.current_event is None else form.current_event.id
		event = Event.query.filter_by(name=name.data).first()
		if event and event.id != current_event_id:
			raise ValidationError(gettext("Name already taken!"))

	def __init__(self, current_event=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.current_event = current_event


def validate_youtube_link(_, link):
	if len(link.data) == 0:
		return
	if not is_youtube_link(link.data):
		raise ValidationError(gettext('Must be a youtube link'))


class VideoForm(Form):
	sport = HiddenField('Sport')
	video = StringField('video', validators=[validate_youtube_link])


class EditVideosForm(FlaskForm):
	videos = FieldList(FormField(VideoForm))
	submit = SubmitField('Update')

