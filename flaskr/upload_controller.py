import os
import pathlib
import traceback

from flask import current_app, send_from_directory, request, flash, redirect
from werkzeug.utils import secure_filename

from flaskr.image_service import add_image_db
from flaskr.project_service import get_project_id, add_project
from flaskr.submissionForms import UploadForm
from PIL import Image
# from config.config import ALLOWED_EXTENSIONS


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
                            "Did you already upload this photo? A file already exists in here with that name.",
                            "danger")
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

                    add_project(project_name, project_path[path_slice:], owners_email, town, date)
                    print("New project created!")

                    # flash("Your images were successfully uploaded your new project!", 'success')
                except Exception as e:
                    print(e)
                    print(traceback.format_exception(None, e, e.__traceback__))
                    flash("Unable to add project", 'warning')
                    return redirect(request.url)
            else:
                project_path = os.path.join(project_upload_path, project_name)

            try:

                for image in uploaded_images:
                    image_filename = secure_filename(image.filename)
                    image_path = os.path.join(project_path, image_filename)
                    image.save(image_path)

                    #img = Image.open(image_path)
                    #img = img.resize((2048, 1152), resample=None, box=None, reducing_gap=None)

                    #img.save(image_path)

                    print("project name: "+project_name)

                    # image_path[6:] is to splice off the "flaskr" from path
                    add_image_db(image_path=image_path[path_slice:], filename=image_filename, project_name=project_name,
                                 project_id=get_project_id(project_name))

                flash("Your images were successfully uploaded your new project!", 'success')
                return redirect(request.url)
            except Exception as e:
                print(e)
                print(traceback.format_exception(None, e, e.__traceback__))
                flash("Unable to upload images", 'warning')
                return redirect(request.url)
        else:
            flash('No image selected')
            return redirect(request.url)

    except Exception as e:
        print(e)
        flash("Your image could not be uploaded", 'danger')
        return redirect(request.url)

