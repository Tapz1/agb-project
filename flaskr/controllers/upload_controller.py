import os
import pathlib
import traceback

from flask import current_app, send_from_directory, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from flaskr.services.image_service import add_image_db
from flaskr.services.project_service import get_project_id, add_project
from PIL import Image



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.app_context().app.config['ALLOWED_EXTENSIONS']


def download_file(name):
    return send_from_directory(current_app.app_context().app.config['UPLOAD_FOLDER'], name)


def upload_multiple_images(image_form, existing_photos, isNew, project_name):
    """for projects"""
    project_path = ""
    path_slice = current_app.app_context().app.config['PATH_SLICE']
    project_upload_path = current_app.app_context().app.config['UPLOAD_FOLDER']
    try:
        if 'image' not in request.files:
            flash('No file')
            return redirect(request.url)

        # multiple photo upload
        uploaded_images = request.files.getlist(image_form.image.name)

        if uploaded_images:
            for image in uploaded_images:
                if allowed_file(image.filename):
                    filename = image.filename
                    if filename in existing_photos:
                        flash(
                            f"Did you already upload this photo? An image already exists in here with the name: {filename}",
                            "warning")
                        return redirect(request.url)
            if isNew:
                image_filename = []
                # creating a new project #

                project_name = request.form['new_project']
                owners_email = request.form['owners_email']
                town = request.form['town']
                date = request.form['project_date']
                try:
                    pathlib.Path(project_upload_path, project_name).mkdir(
                        exist_ok=False)
                except Exception as e:
                    print(e)
                    flash("There's already an existing project with that name", 'danger')
                    return redirect(request.url)

                try:
                    project_path = os.path.join(project_upload_path, project_name)
                    project_id = int(os.urandom(4).hex(), 16)
                    add_project(project_id, project_name, project_path[path_slice:], owners_email, town, date)
                    print("New project created!")

                    # flash("Your images were successfully uploaded your new project!", 'success')
                except Exception as e:
                    print(e)
                    print(traceback.format_exception(None, e, e.__traceback__))
                    flash("Unable to add project", 'warning')
                    # return redirect(request.url)
            else:
                project_path = os.path.join(project_upload_path, project_name)

            try:

                for image in uploaded_images:
                    #image_filename = secure_filename(image.filename)
                    new_filename = secure_filename(f"{project_name}_{os.urandom(3).hex()}")
                    image_path = os.path.join(project_path, new_filename)
                    image.save(image_path)

                    img = Image.open(image_path)

                    img.save(image_path, "JPEG", optimize=True)     # optimizes images

                    print("project name: "+project_name)
                    project_id = get_project_id(project_name)

                    # image_path[6:] is to splice off the "flaskr" from path
                    image_id = int(os.urandom(4).hex(), 16)
                    add_image_db(image_id=image_id, image_path=image_path[path_slice:], filename=new_filename, project_name=project_name,
                                 project_id=project_id)

                flash("Your images were successfully uploaded your new project!", 'success')
                redirect(url_for("blueprint.view_project", project_name=project_name))
            except Exception as e:
                print(e)
                print(traceback.format_exception(None, e, e.__traceback__))
                flash("Unable to upload images", 'danger')
                # return redirect(request.url)
        else:
            flash('No image selected')
            # return redirect(request.url)

    except Exception as e:
        print(e)
        flash("Your image could not be uploaded", 'danger')
        # return redirect(request.url)


def upload_bg_image(page_name):
    static_path = current_app.app_context().app.config['STATIC_PATH']
    print(f"page_name: {page_name}")
    page_filename = ""
    if page_name == 'home':
        page_filename = "home-bg.jpg"
    elif page_name == 'gallery':
        page_filename = "gallery-bg.jpg"
    elif page_name == 'contact':
        page_filename = "contact-bg.jpg"
    elif page_name == 'testimonials':
        page_filename = "testimonials-bg.jpg"
    elif page_name == 'login':
        page_filename = "login-bg.jpg"

    print(f"page_filename: {page_filename}")

    try:
        if 'bg_image' not in request.files:
            flash('No file', 'warning')
            return redirect(request.url)
        image = request.files['bg_image']

        if image.filename == '':
            flash('No image selected', 'warning')
            print("no image selected")
            return redirect(request.url)

        if image and allowed_file(image.filename):
            #filename = secure_filename(image.filename)

            image_path = os.path.join(static_path, "background-images", page_filename)
            image.save(image_path)

            img = Image.open(image_path)        # can go straight into Pillow since filename already in system
            img.save(image_path, "JPEG", optimize=True)  # optimizes images

            flash("Your image was uploaded as a background image!", 'success')
            return redirect(request.url)

    except Exception as e:
        print(e)
        flash("Your image could not be uploaded", 'danger')
        return redirect(request.url)



