import traceback

from werkzeug.utils import secure_filename

from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, redirect, url_for, flash, current_app, request
from flaskr.upload_controller import allowed_file
from flaskr.project_service import get_all_projects, delete_project_row, get_project_id, get_project_name
from flaskr.image_service import add_image_db, delete_image_db, get_all_images, get_images_from_project
from flaskr.submissionForms import UploadForm
import os
from PIL import Image   # needs to get commented out during production


@DecoratorWraps.is_logged_in
def delete_image(image_id, project_id, filename):
    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    project_name = ""
    try:
        project_name = get_project_name(project_id)
        file_path = os.path.join(upload_folder, project_name, filename)
        os.remove(file_path)
        delete_image_db(image_id)
        flash("Image deleted!", "success")

    except Exception as e:
        print(e)
        flash("Image could not be deleted!", "danger")
    return redirect(url_for("blueprint.view_project", project_id=project_id))


