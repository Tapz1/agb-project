from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, request, redirect, url_for, flash, current_app

from flaskr.controllers.testimonial_controller import get_testimonials
# from config.config import CLIENT_EMAIL
from flaskr.services.testimonial_service import delete_entry, update_approval
from flaskr.services.mail_service import MailService
from flaskr.models.submissionForms import RequestTestimonial, UploadForm
from flaskr.controllers.upload_controller import upload_multiple_images
import os


@DecoratorWraps.is_logged_in
def admin_portal():
    session.modified = True
    project_names = []

    email = session.get("email")
    if email == current_app.app_context().app.config['CLIENT_EMAIL']:
        name = "Allan"
    else:
        name = "Chris"

    form = RequestTestimonial(request.form)
    request_email = form.email.data

    image_form = UploadForm()

    ms = MailService()

    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    # upload_folder = url_for('static', filename='uploads')
    existing_photos = os.listdir(upload_folder)

    pending = None

    try:
        pending = get_testimonials('pending')
    except Exception as e:
        print(e)

    if request.method == 'POST':
        print("POST request detected")
        if "send-request" in request.form and form.validate():
            print("send button pressed")
            ms.send_testimonial_request(request_email)
            flash('Your request has been sent successfully!', 'success')
            return redirect(request.url)

        if "upload-image" in request.form:
            # print("* upload button pressed *")
            upload_multiple_images(image_form=image_form, existing_photos=existing_photos, isNew=True, project_name="")

    return render_template("admin.html", name=name, email=email, title="Admin", form=form,
                           image_form=image_form, pending_testimonials=pending)


@DecoratorWraps.is_logged_in
def approve_testimonial(testimonial_id):

    try:
        update_approval(testimonial_id)
        flash("Testimonial approved!", "success")
        return redirect(url_for("blueprint.admin_portal"))
    except Exception as e:
        print(e)
        error = "Testimonial could not be approved"
        flash(error, "danger")
        return redirect(url_for("blueprint.admin_portal"))


@DecoratorWraps.is_logged_in
def delete_testimonial_request(testimonial_id):

    try:
        delete_entry(testimonial_id)
        flash("Testimonial deleted!", "success")
        return redirect(url_for("blueprint.admin_portal"))
    except Exception as e:
        print(e)
        error = "Testimonial could not be deleted"
        flash(error, "danger")
        return redirect(url_for("blueprint.admin_portal"))


@DecoratorWraps.is_logged_in
def delete_testimonial(testimonial_id):

    try:
        delete_entry(testimonial_id)
        flash("Testimonial deleted!", "success")
        return redirect(url_for("blueprint.testimonials"))
    except Exception as e:
        print(e)
        error = "Testimonial could not be deleted"
        flash(error, "danger")
        return redirect(url_for("blueprint.testimonials"))

