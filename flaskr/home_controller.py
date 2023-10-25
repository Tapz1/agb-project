from flask import render_template, session
from flaskr.testimonial_service import get_limited_approved


def home():
    session.modified = True

    try:
        testimonial_highlights = get_limited_approved()

        if len(testimonial_highlights) == 0:
            print("No testimonials")

        return render_template("home.html", testimonials=testimonial_highlights)

    except Exception as e:
        print("Error with getting testimonial highlights")
        print(e)

    return render_template("home.html")




