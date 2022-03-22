from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, FileField, SubmitField
from wtforms.validators import Length, DataRequired


class AccountSettingsForm(FlaskForm):
    email = EmailField('Email', validators=[Length(max=120)])
    password = PasswordField('New password', validators=[Length(max=80)])
    confirm_password = PasswordField('Confirm new password', 
                                    validators=[Length(max=80)])
    current_password = PasswordField('Current password', 
                                validators=[DataRequired(), Length(max=80)])
    submit_account_settings = SubmitField('Submit')


class UserSettingsForm(FlaskForm):
    profile_picture = FileField('Profile picture', validators=[])
    profile_color = StringField('Profile color', validators=[Length(min=7, max=7)])
    username = StringField('Username', validators=[Length(max=80)])
    submit_user_settings = SubmitField('Submit')
