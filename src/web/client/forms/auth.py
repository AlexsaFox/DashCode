from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=80)])
    email = EmailField('Email', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=80)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(max=80)])
    submit_registration = SubmitField('Submit')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=80)])
    submit_login = SubmitField('Submit')
