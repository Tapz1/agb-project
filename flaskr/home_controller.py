from flask import render_template, session, flash, request

from flaskr.project_controller import get_all_project_thumbnails
from flaskr.project_service import get_limited_projects
from flaskr.testimonial_controller import get_limited_testimonials
from flaskr.submissionForms import UploadForm
from flaskr.upload_controller import upload_bg_image
import traceback as tb


def home():
    session.modified = True
    projects = []
    project_thumbnails = []
    testimonial_highlights = []
    first_testimonial = None
    enumerated_testimonials = []

    image_form = UploadForm()

    try:
        projects = get_limited_projects(8)

        # projects & thumbnails binding
        project_thumbnails = get_all_project_thumbnails(projects)

    except Exception as e:
        print(e)
        print(tb.format_exception(None, e, e.__traceback__))
        flash("Unable to get binded projects & thumbnails", 'danger')

    try:
        testimonial_highlights = get_limited_testimonials(2)

        if len(testimonial_highlights) == 0:
            print("No testimonials")

        if len(testimonial_highlights) > 0:
            first_testimonial = testimonial_highlights[0]
            enumerated_testimonials = [*range(0, len(testimonial_highlights))]  # for carousel indicators
        print(f"photos len: {len(testimonial_highlights)}")

    except Exception as e:
        print("Error with getting testimonial highlights")
        print(e)

    if request.method == 'POST' and "upload-image" in request.form:
        print("upload bg attempted")
        upload_bg_image(page_name="home")

    return render_template("home.html", testimonials=testimonial_highlights, first_testimonial=first_testimonial,
                           project_data=zip(projects, project_thumbnails), enumerated_testimonials=enumerated_testimonials, image_form=image_form)




