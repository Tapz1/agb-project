from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, redirect, url_for, flash, current_app
from flaskr.controllers.project_controller import get_project_item
from flaskr.services.image_service import delete_image_db, get_image_by_id, get_limited_images_db, update_check_db, \
    get_checked_images_db
import os


@DecoratorWraps.is_logged_in
def delete_image(image_id, project_id, filename):
    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    if DecoratorWraps.is_logged_in:
        try:
            project_name = get_project_item(project_id, "project_name")
            file_path = os.path.join(upload_folder, project_name, filename)
            os.remove(file_path)
            delete_image_db(image_id)
            flash("Image deleted!", "success")

        except Exception as e:
            print(e)
            flash("Image could not be deleted!", "danger")
        return redirect(url_for("blueprint.view_project", project_id=project_id))


def view_image(image_id):
    image = get_image_by_id(image_id)
    image_path = image[2]
    filename = image[3]
    project_name = image[4]
    project_id = image[5]

    return render_template("view_image.html", image_path=image_path, filename=filename,
                           image_id=image_id, project_name=project_name, project_id=project_id)


def get_limited_images(limit):
    return get_limited_images_db(limit)


def get_checked_images():
    return get_checked_images_db()


@DecoratorWraps.is_logged_in
def update_check_image(image_id, isChecked, project_id):
    if isChecked == '0':
        flash("Image removed from Gallery slideshow", "success")
    elif isChecked == '1':
        flash("Image added to Gallery slideshow!", "success")
    update_check_db(image_id, isChecked)
    return redirect(url_for("blueprint.view_project", project_id=project_id))
