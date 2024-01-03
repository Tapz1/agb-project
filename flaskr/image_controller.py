from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, redirect, url_for, flash, current_app, request
from flaskr.project_controller import get_project_item
from flaskr.image_service import delete_image_db, update_check_db, \
    get_checked_images_db, get_image_by_name
import os
import traceback as tb

@DecoratorWraps.is_logged_in
def delete_image(image_id, project_id, filename):
    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    project_name = ""
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
        return redirect(url_for("blueprint.view_project", project_name=project_name))


def view_image(filename):
    image = get_image_by_name(filename)
    image_path = image[2]
    image_id = image[3]
    project_name = image[4]
    project_id = image[5]

    return render_template("view_image.html", image_path=image_path, filename=filename,
                           image_id=image_id, project_name=project_name, project_id=project_id, title=f"viewing {filename}")


def get_checked_images():
    return get_checked_images_db()


@DecoratorWraps.is_logged_in
def update_check_image(image_id, isChecked):
    try:
        if isChecked == '0':
            flash("Image removed from Gallery slideshow", "success")
        elif isChecked == '1':
            flash("Image added to Gallery slideshow!", "success")
        update_check_db(image_id, isChecked)
    except Exception as e:
        flash("Unable to add to slideshow", "danger")
        print(e)
        print(tb.format_exception(None, e, e.__traceback__))
    return redirect(request.referrer)
