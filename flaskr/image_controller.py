import traceback

from werkzeug.utils import secure_filename

from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, redirect, url_for, flash, current_app, request

from flaskr.upload_controller import allowed_file
from flaskr.upload_service import get_projects, delete_project_row
from flaskr.submissionForms import UploadForm
import os


@DecoratorWraps.is_logged_in
def view_all_projects():
    session.modified = True

    try:
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']

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
            
            #flat_list = [item for sublist in photo_list for item in sublist]
            #flat_list_names = [item for sublist in photo_list_names for item in sublist]
            # all_photos=zip(flat_list, flat_list_names)
        """

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
    session.modified = True
    image_form = UploadForm()

    try:
        project_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], project_name)
        existing_photos = os.listdir(project_folder)
        photo_names = [photo for photo in existing_photos]
        photos = [f'uploads/{project_name}/' + photo for photo in existing_photos]
        print(f'uploads/{project_name}')

        if request.method == 'POST':
            if "upload-image" in request.form:
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
                        try:
                            for image in uploaded_images:
                                image_filename = secure_filename(image.filename)
                                image.save(os.path.join(project_folder, image_filename))

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

        return render_template("view_project.html", project_name=project_name, all_photos=zip(photos, photo_names),
                               image_form=image_form)

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