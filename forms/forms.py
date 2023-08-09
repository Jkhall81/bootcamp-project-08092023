from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import Email, ValidationError
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
# <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>

class UserRegistrationForm(Form):
	name = StringField('Name', validators=[validators.InputRequired()])
	email = StringField('Email', validators=[validators.InputRequired(), Email()])
	password = PasswordField('Password', validators=[validators.InputRequired(), validators.EqualTo('confirm_password', message='Passowrds must match')])
	confirm_password = PasswordField('Confirm Password', validators=[validators.InputRequired()])
	bio = TextAreaField('Bio')


class AddMovieForm(Form):
	moviename = StringField('Name', validators=[validators.InputRequired()])


class LoginForm(Form):
	email = StringField('Email', validators=[validators.InputRequired(), Email()])
	password = PasswordField('Password', validators=[validators.InputRequired()])


class EditUserForm(Form):
	name = StringField('Name', validators=[validators.InputRequired()])
	email = StringField('Email', validators=[validators.InputRequired(), Email()])
	bio = TextAreaField('Bio')


class MovieCommentForm(Form):
	email = StringField('Email', validators=[validators.InputRequired(), Email()])
	subject = StringField('Subject', validators=[validators.InputRequired()])
	comment_text = TextAreaField('Review')


class EditCommentForm(Form):
	email = StringField('Email', validators=[validators.InputRequired(), Email()])
	subject = StringField('Subject', validators=[validators.InputRequired()])
	comment_text = TextAreaField('Review')
	