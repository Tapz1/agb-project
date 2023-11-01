import traceback
from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, redirect, url_for, flash, current_app
from flaskr.upload_service import get_projects, delete_project_row, get_project_id
import os


@DecoratorWraps.is_logged_in
def view_all_projects():
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

        all_projects = os.listdir(upload_folder)

        photo_thumbnails = []

        for project in projects:
            project_photos = os.listdir(os.path.join(upload_folder, project[1]))
            first_photo_path = url_for('static', filename='Placeholder_view_vector.svg.png')
            if len(project_photos) > 0:
                print("project_photos[0]: " + project_photos[0])
                folder = os.path.join('uploads', project[1], project_photos[0])
                first_photo_path = url_for('static', filename='uploads/' + project[1] + '/' + project_photos[0])
            print("first_photo_path: " + first_photo_path)
            photo_thumbnails.append(first_photo_path)


        """this may be good for the gallery page to pull all photos"""
        """
        for project in projects:
            project_photos = os.listdir(os.path.join(upload_folder, project[1]))          # 2 = project path
            photo_names = [photo for photo in project_photos]
            photo_list_names.append(photo_names)

            print(project[1])
            print(project[2])
            project_name = 'uploads/' + project[1] + '/'                                  # 1 = project name
            photos = [project_name + photo for photo in project_photos]

            photo_list.append(photos)
        """

        #flat_list = [item for sublist in photo_list for item in sublist]
        #flat_list_names = [item for sublist in photo_list_names for item in sublist]
        # all_photos=zip(flat_list, flat_list_names)

        # latest_photo = "uploads/" + max(glob.glob(upload_folder))
        # print(enumerated_photos)
        return render_template("view_all_projects.html",
                               upload_folder=upload_folder, all_projects=all_projects, projects=projects,
                               project_data=zip(projects, photo_thumbnails))

    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))

    return render_template("view_all_projects.html")


@DecoratorWraps.is_logged_in
def view_project(project_name):
    try:
        project_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], project_name)
        photos = os.listdir(project_folder)
        photo_names = [photo for photo in photos]
        photos = [f'uploads/{project_name}/' + photo for photo in photos]
        print(f'uploads/{project_name}')
        return render_template("view_project.html", project_name=project_name, all_photos=zip(photos, photo_names))

    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))


@DecoratorWraps.is_logged_in
def delete_image(project_name, filename):
    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, project_name, filename)
    print(file_path)
    try:
        os.remove(file_path)
        flash("Image deleted!", "success")
        return redirect(url_for("blueprint.view_all_projects"))
    except Exception as e:
        print(e)
        flash("Image could not be deleted!", "danger")
        return redirect(url_for("blueprint.view_all_projects"))


@DecoratorWraps.is_logged_in
def delete_project(project_id, project_name):
    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, project_name)
    print(file_path)
    try:
        #project_id = get_project_id(project_name)
        delete_project_row(project_id)
        os.rmdir(file_path)
        flash("Project deleted!", "success")
        return redirect(url_for("blueprint.view_all_projects"))
    except Exception as e:
        print(e)
        flash("Project could not be deleted!", "danger")
        return redirect(url_for("blueprint.view_all_projects"))