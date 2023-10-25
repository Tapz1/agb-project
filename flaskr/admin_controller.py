from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, request, redirect, url_for, flash, current_app
# from config.config import CLIENT_EMAIL
from flaskr.testimonial_service import get_all_pending, delete_entry, update_approval
from flaskr.mail_service import MailService
from flaskr.submissionForms import RequestTestimonial, UploadForm
from flaskr.upload_controller import allowed_file
from flaskr.upload_service import get_projects, add_project
import os
import traceback
import pathlib
from PIL import Image
from werkzeug.utils import secure_filename


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

    # new project
    new_project_name = image_form.new_project.data
    owners_email = image_form.owners_email.data
    town = image_form.town.data
    date = image_form.project_date.data


    #if not new_project_name == "":



    ms = MailService()

    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    # upload_folder = url_for('static', filename='uploads')
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
                uploaded_images = request.files.getlist(image_form.image.name)
                new_project_name = request.form['new_project']
                owners_email = request.form['owners_email']
                town = request.form['town']
                date = request.form['project_date']

                print(new_project_name)
                print(owners_email)
                print(town)
                print(date)
                if uploaded_images:
                    for image in uploaded_images:
                        if allowed_file(image.filename):
                            filename = image.filename
                            if filename in existing_photos:
                                flash(
                                    "Did you already upload this photo? A file already exists in here with that name.",
                                    "danger")
                                return redirect(request.url)
                    if new_project_name != "":
                        image_filename = []
                        # creating a new project
                        try:
                            pathlib.Path(upload_folder, new_project_name).mkdir(exist_ok=False)
                        except Exception as e:
                            print(e)
                            flash("There's already an existing project with that name", 'danger')
                            return redirect(request.url)

                        try:
                            project_path = os.path.join(upload_folder, new_project_name)
                            for image in uploaded_images:
                                image_filename = secure_filename(image.filename)
                                image.save(os.path.join(project_path, image_filename))

                            add_project(new_project_name, project_path, owners_email, town, date)

                            flash("Your images were successfully uploaded your new project!", 'success')
                            return redirect(request.url)
                        except Exception as e:
                            print(e)
                            print(traceback.format_exception(None, e, e.__traceback__))
                            flash("Unable to add project", 'warning')
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

