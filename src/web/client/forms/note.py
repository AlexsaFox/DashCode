from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField,SelectField, URLField
from wtforms.validators import DataRequired, Length, URL

class NoteCreateForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired(), Length(max=65)])
    context = TextAreaField('Context', validators=[DataRequired()])
    link = URLField('Link', validators=[])
    submit = SubmitField('Create')

class NoteEditForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired(), Length(max=65)])
    context = TextAreaField('Context', validators=[DataRequired()])
    link = URLField('Link', validators=[])
    privacy = SelectField('Privacy', choices=[('private', 'Private'),
                                              ('public', 'Public')],
                                              validators=[DataRequired()])
    submit = SubmitField('Save')

class NoteRemoveForm(FlaskForm):
    submit = SubmitField('Remove')
