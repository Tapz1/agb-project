import os

from flask import render_template, redirect, flash, url_for, request, session

from flaskr.controllers.upload_controller import upload_bg_image
from flaskr.services.project_service import project_exists, get_project_id_by_email
from flaskr.services.testimonial_service import (get_all_approved, paginate_approved, add_testimonial, get_testimonial_id_by_email,
                                                 get_all_pending, get_limited_approved, add_project_id)
from flaskr.services.mail_service import MailService
from flaskr.services.token_service import confirm_token
from flaskr.models.submissionForms import TestimonialForm, UploadForm
from flask_paginate import get_page_parameter, Pagination


def testimonials():
    session.modified = True

    all_testimonials = []
    pagination = None
    paginated_data = []

    image_form = UploadForm()

    try:
        all_testimonials = get_testimonials('approved')
    except Exception as e:
        print("Error with getting testimonials")
        print(e)

    try:        # looks for any existing projects with the same email in a testimonial
        for testimonial in all_testimonials:
            email = testimonial[2]
            if project_exists(email) > 0:
                print("Project exists with same email in testimonials")
                add_project_id(project_id=get_project_id_by_email(email),
                                 testimonial_id=get_testimonial_id_by_email(email))
    except Exception as e:
        print("Unable to attach project ids")
        print(e)

    try:
        search = False
        q = request.args.get('q')
        if q:
            search = True

        # setting pagination config
        page = request.args.get(get_page_parameter(), type=int, default=1)
        limit = 3  # per page
        offset = page * limit - limit

        paginated_data = paginate_approved(limit=limit, offset=offset)

        pagination = Pagination(page=page, total=len(all_testimonials), search=search, record_name='testimonials',
                                per_page=limit, css_framework='bootstrap', alignment='center', bs_version='5')

    except Exception as e:
        print("Error paginating")
        print(e)

    if request.method == 'POST' and "upload-image" in request.form:
        print("upload bg attempted")
        upload_bg_image(page_name="testimonials")

    return render_template("testimonials.html", title="Testimonials", testimonials=paginated_data,
                           pagination=pagination, image_form=image_form)


def testimonial_form(token):

    try:
        confirmed_email = confirm_token(token)

        if not confirmed_email:
            flash("The link is invalid or has expired.", "danger")
            return redirect(url_for("blueprint.home"))

    except Exception as e:
        print(e)
        flash("The link is invalid or has expired.", "danger")
        return redirect(url_for("blueprint.home"))

    form = TestimonialForm(request.form, email=confirmed_email)
    name = form.name.data
    email = form.email.data
    message = form.message.data
    town = form.town.data

    ms = MailService()

    if request.method == 'POST':
        if form.validate():
            testimonial_id = int(os.urandom(4).hex(), 16)
            print(f"testimonial_id: {testimonial_id}")
            add_testimonial(testimonial_id, name, email, message, town)
            ms.send_testimonial_email(name, email, message, town)
            ms.testimonial_receipt(name, email, message, town)

            try:
                if project_exists(email) > 0:
                    print("Project exists with same email")
                    add_project_id(project_id=get_project_id_by_email(email), testimonial_id=get_testimonial_id_by_email(email))
            except Exception as e:
                print("Issue with adding project_id to testimonial")
                print(e)
            flash("Your testimonial was successfully sent for approval", 'success')
            return redirect(url_for("blueprint.home"))
        else:
            error = "Testimonial could not be submitted"
            flash(error, "danger")
            return render_template('testimonial_form.html', form=form, title="Add Testimonial")
    return render_template("testimonial_form.html", form=form, title="Add Testimonial")


def get_testimonials(option, limit=""):
    """
    encapsulation for db
        option can be pending or approved
    """
    if option == 'pending':
        return get_all_pending()
    elif option == 'approved':
        return get_all_approved()


def get_limited_testimonials(limit):
    return get_limited_approved(limit)

