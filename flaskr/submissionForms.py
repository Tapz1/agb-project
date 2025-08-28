from wtforms import (StringField, validators, Form, TextAreaField, EmailField,
                     FileField, MultipleFileField, SelectField, DateField, BooleanField)
from datetime import date


class TestimonialForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email(message='Must be a valid email address')],
                       id='email', render_kw={'readonly': True})
    town = StringField('Town', [validators.Length(min=3, max=50)], id='town')
    message = TextAreaField('Message', [validators.Length(min=90, max=5000)])

    # state = StringField('State', [validators.Length(min=2, max=2)], id='state')


class RequestTestimonial(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)], id='name')
    email = EmailField('', [validators.DataRequired(), validators.Email(message='Must be a valid email address')], id='email')


class UploadForm(Form):
    bg_image = FileField(u'Change Background', [validators.DataRequired()])
    project = SelectField(u'Project Info', choices=[])
    image = MultipleFileField('Upload Images', [validators.DataRequired()])
    new_project = StringField('Project Name')
    owners_email = EmailField("Owner's Email", [validators.Email(message='Must be a valid email address')])
    town = StringField("Town", [validators.Length(min=3, max=50)])
    project_date = DateField("Project Date", [validators.Length(min=1)], default=date.today)
    isChecked = BooleanField("Add to Gallery slideshow", default=False)
    # description = TextAreaField(u'Image Description')


class GalleryDropdowns(Form):
    sort_by = SelectField('Sort By', choices=[("DESC", "Latest"), ("ASC", "Oldest")], id='sort')
    filter_by = SelectField('Filter By Town', id='filter')
