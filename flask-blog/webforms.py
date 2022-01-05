from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")


class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = CKEditorField('Content', validators=[DataRequired()])
	slug = StringField("Slug")
	author = StringField("Author")
	submit = SubmitField("Submit")


class NamerForm(FlaskForm):
	name = StringField("Whats Your Name?", validators=[DataRequired()])
	submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired()])
	password_hash = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")


class UserForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	about_author = TextAreaField("About Author")
	email = StringField("Email:", validators=[DataRequired()])
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Submit")



