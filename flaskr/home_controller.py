from flask import render_template, session, flash, request

from flaskr.project_controller import get_all_project_thumbnails
from flaskr.project_service import get_limited_projects
from flaskr.testimonial_controller import get_limited_testimonials
from flaskr.submissionForms import UploadForm
from flaskr.upload_controller import upload_bg_image
import traceback as tb


def home():
    session.modified = True

    image_form = UploadForm()

    if request.method == 'POST' and "upload-image" in request.form:
        print("upload bg attempted")
        upload_bg_image(page_name="home")

    return render_template("home.html", image_form=image_form)




