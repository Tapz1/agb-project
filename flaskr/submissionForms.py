import os.path
import re
import email_validator
from wtforms import (StringField, validators, Form, ValidationError, PasswordField, TextAreaField, TelField, EmailField,
                     FileField, SubmitField, MultipleFileField, SelectField, DateField)
from datetime import date
from wtforms.validators import Regexp


class TestimonialForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=40)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email(message='Must be a valid email address')], id='email', render_kw={'readonly': True})
    town = StringField('Town', [validators.Length(min=3, max=40)], id='town')
    message = TextAreaField('Message', [validators.Length(min=90, max=5000)])

    # state = StringField('State', [validators.Length(min=2, max=2)], id='state')


class RequestTestimonial(Form):
    email = EmailField('', [validators.DataRequired(), validators.Email(message='Must be a valid email address')])


class UploadForm(Form):
    #image = FileField('Image', [validators.DataRequired()])
    project = SelectField(u'Project', choices=[])
    image = MultipleFileField('', [validators.DataRequired()])
    project_type = SelectField('', coerce=str, choices=[("new", "New"), ("existing", "Existing")], id='p_type')
    new_project = StringField('Project Name')
    owners_email = EmailField("", [validators.Email(message='Must be a valid email address')])
    town = StringField("", [validators.Length(min=3, max=40)])
    project_date = DateField("", default=date.today)
    # description = TextAreaField(u'Image Description')

