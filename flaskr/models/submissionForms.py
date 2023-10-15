import os.path
import re

from wtforms import StringField, validators, Form, ValidationError, PasswordField, TextAreaField, TelField, EmailField, FileField, SubmitField
from wtforms.validators import Regexp


class RecaptchaField:
    pass


class ContactForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=20)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email(message='Must be a valid email address')])
    phone = TelField('Phone Number', [validators.DataRequired(), validators.Length(min=10, max=14), Regexp(regex='^[+-]?[0-9]+$')])
    contact_message = TextAreaField('Message', [validators.DataRequired(), validators.Length(min=20, max=400)])
    #recaptcha = RecaptchaField()


class TestimonialForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=40)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email(message='Must be a valid email address')], id='email', render_kw={'readonly': True})
    message = TextAreaField('Message', [validators.Length(min=90, max=5000)])
    city = StringField('City', [validators.Length(min=3, max=40)], id='city')
    state = StringField('State', [validators.Length(min=2, max=2)], id='state')


class RequestTestimonial(Form):
    email = EmailField('', [validators.DataRequired(), validators.Email(message='Must be a valid email address')])


class UploadForm(Form):
    image = FileField('Image', [validators.DataRequired()])
    # description = TextAreaField(u'Image Description')