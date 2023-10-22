from werkzeug.utils import secure_filename

from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, request, redirect, url_for, flash, current_app
# from config.config import CLIENT_EMAIL
from flaskr.services.testimonial_service import get_all_pending, delete_entry, update_approval
from flaskr.services.mail_service import MailService
from flaskr.models.submissionForms import RequestTestimonial, UploadForm
from flaskr.controllers.upload_controller import allowed_file
from flaskr.services.upload_service import get_projects
import os
from PIL import Image  # has to be commented out when deployed


@DecoratorWraps.is_logged_in
def admin_portal():
    session.modified = True
    project_names = []

    email = session.get("email")
    if email == current_app.app_context().app.config['CLIENT_EMAIL']:
        name = "Brandon"
    else:
        name = "Chris"

    try:
        project_names = get_projects()
    except Exception as e:
        print("Couldn't get projects")
        print(e)

    form = RequestTestimonial(request.form)
    request_email = form.email.data

    image_form = UploadForm()
    image_form.project.choices = project_names



    ms = MailService()

    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    existing_photos = os.listdir(upload_folder)

    pending = None

    try:
        pending = get_all_pending()
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

            try:
                if 'image' not in request.files:
                    flash('No file')
                    return redirect(request.url)

                # multiple photo upload
                images = request.files.getlist(image_form.image.name)
                if images:
                    for image in images:
                        if allowed_file(image.filename):
                            filename = image.filename
                            if filename in existing_photos:
                                flash(
                                    "Did you already upload this photo? A file already exists in here with that name.",
                                    "danger")
                                return redirect(request.url)
                            else:
                                image_path = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'],
                                                          filename)
                                image.save(image_path)
                    flash("Your images were successfully uploaded!", 'success')
                    return redirect(request.url)
                else:
                    flash('No image selected')
                    return redirect(request.url)

            except Exception as e:
                print(e)
                flash("Your image could not be uploaded", 'danger')
                return redirect(request.url)

    return render_template("admin.html", name=name, email=email, title="Admin", form=form,
                           image_form=image_form, pending_testimonials=pending)


@DecoratorWraps.is_logged_in
def add_project():
    pass


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

