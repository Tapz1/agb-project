from flask import render_template, session, flash

from flaskr.project_controller import get_all_project_thumbnails
from flaskr.project_service import get_limited_projects
from flaskr.testimonial_controller import get_limited_testimonials
import traceback as tb


def home():
    session.modified = True
    projects = []
    project_thumbnails = []
    testimonial_highlights = []

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

    except Exception as e:
        print("Error with getting testimonial highlights")
        print(e)

    return render_template("home.html", testimonials=testimonial_highlights, project_data=zip(projects, project_thumbnails))




