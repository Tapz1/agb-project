
from flask import render_template, request, session

from flaskr.upload_controller import upload_bg_image
from flaskr.submissionForms import UploadForm


def contact():
    session.modified = True
    image_form = UploadForm()

    if request.method == 'POST' and "upload-image" in request.form:
        upload_bg_image(page_name="contact")

    return render_template("contact.html", image_form=image_form, title="Contact Us")
