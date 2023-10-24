import traceback
from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, request, redirect, url_for, flash, current_app
from flaskr.services.upload_service import get_projects
import os


@DecoratorWraps.is_logged_in
def view_images():
    session.modified = True

    paths = []

    photo_list = []
    photo_list_names = []
    try:
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
        #photos = os.listdir(upload_folder)
        #photo_names = [photo for photo in photos]
        #photos = ['uploads/' + photo for photo in photos]

        projects = get_projects()
        print('test')

        for project in projects:
            project_photos = os.listdir(os.path.join(upload_folder, project[1]))          # 2 = project path
            photo_names = [photo for photo in project_photos]
            photo_list_names.append(photo_names)

            print(project[1])
            print(project[2])
            project_name = 'uploads/' + project[1] + '/'    # 1 = project name
            photos = [project_name + photo for photo in project_photos]

            photo_list.append(photos)

        flat_list = [item for sublist in photo_list for item in sublist]
        flat_list_names = [item for sublist in photo_list_names for item in sublist]

        # latest_photo = "uploads/" + max(glob.glob(upload_folder))
        # print(enumerated_photos)
        return render_template("view_images.html", all_photos=zip(flat_list, flat_list_names), upload_folder=upload_folder)

    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))

    return render_template("view_images.html")


@DecoratorWraps.is_logged_in
def delete_image(filename):
    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, filename)
    print(file_path)
    try:
        os.remove(file_path)
        flash("Image deleted!", "success")
        return redirect(url_for("blueprint.view_images"))
    except Exception as e:
        print(e)
        flash("Image could not be deleted!", "danger")
        return redirect(url_for("blueprint.view_images"))