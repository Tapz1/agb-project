
from flask import render_template, redirect, flash, url_for, request, session
from flaskr.services.testimonial_service import get_all_approved, paginate_approved, add_testimonial
from flaskr.services.mail_service import MailService
from flaskr.services.token_service import confirm_token
from flaskr.models.submissionForms import TestimonialForm
from flask_paginate import get_page_parameter, Pagination


def testimonials():
    session.modified = True

    all_testimonials = []
    pagination = None
    paginated_data = []

    try:
        all_testimonials = get_all_approved()
    except Exception as e:
        print("Error with getting testimonials")
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

    return render_template("testimonials.html", testimonials=paginated_data, pagination=pagination)


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
            add_testimonial(name, email, message, town)
            ms.send_testimonial_email(name, email, message, town)
            ms.testimonial_receipt(name, email, message, town)
            flash("Your testimonial was successfully sent for approval", 'success')
            return redirect(url_for("blueprint.home"))
        else:
            error = "Testimonial could not be submitted"
            flash(error, "danger")
            return render_template('testimonial_form.html', form=form, title="Add Testimonial")
    return render_template("testimonial_form.html", form=form, title="Add Testimonial")
