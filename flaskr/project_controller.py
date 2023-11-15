import traceback

from werkzeug.utils import secure_filename

from flaskr.decorator_wraps import DecoratorWraps
from flask import render_template, session, redirect, url_for, flash, current_app, request
from flaskr.upload_controller import upload_multiple_images
from flaskr.project_service import delete_project_row, get_project_name, get_all_projects, get_projects_by_town
from flaskr.image_service import get_images_from_project, get_project_thumbnail
from flaskr.submissionForms import UploadForm
from flask_paginate import get_page_parameter, Pagination
import os
import shutil
from PIL import Image   # needs to get commented out during production
import traceback as tb


@DecoratorWraps.is_logged_in
def view_all_projects():
    session.modified = True

    try:
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']

        projects, pagination = get_paginated_projects(sort_by="DESC")
        print('test')

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

        return render_template("view_all_projects.html",
                               upload_folder=upload_folder, projects=projects,
                               project_data=zip(projects, photo_thumbnails))

    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))

    return render_template("view_all_projects.html")


def view_project(project_id):
    session.modified = True
    image_form = UploadForm()
    project_name = get_project_name(project_id)
    print(project_name)

    first_photo = None
    enumerated_photos = []

    try:

        project_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], project_name)
        existing_photos = os.listdir(project_folder)
        photo_names = [photo for photo in existing_photos]
        #photos = [f'uploads/{project_name}/' + photo for photo in existing_photos]\
        photos = get_images_from_project(project_id)
        #print(f'uploads/{project_name}')

        if len(photos) > 0:
            first_photo = photos[0]
            enumerated_photos = [*range(0, len(photos))]  # for carousel indicators
        #print(f"photos len: {len(photos)}")

        if request.method == 'POST':
            if "upload-image" in request.form:
                upload_multiple_images(image_form=image_form, existing_photos=existing_photos, isNew=False, project_name=project_name)

        return render_template("view_project.html", project_name=project_name, all_photos=zip(photos, photo_names),
                               image_form=image_form, photos=photos, first_photo=first_photo, enumerated_photos=enumerated_photos)

    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))
        return redirect(url_for("blueprint.view_all_projects"))



@DecoratorWraps.is_logged_in
def view_project_admin(project_id):
    session.modified = True
    image_form = UploadForm()
    project_name = get_project_name(project_id)
    print(project_name)

    try:

        project_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], project_name)
        existing_photos = os.listdir(project_folder)
        photo_names = [photo for photo in existing_photos]
        #photos = [f'uploads/{project_name}/' + photo for photo in existing_photos]\
        photos = get_images_from_project(project_id)
        print(f'uploads/{project_name}')

        if request.method == 'POST':
            if "upload-image" in request.form:
                upload_multiple_images(image_form=image_form, existing_photos=existing_photos, isNew=False, project_name=project_name)

        return render_template("view_project_admin.html", project_name=project_name, all_photos=zip(photos, photo_names),
                               image_form=image_form, photos=photos)

    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))
        return redirect(url_for("blueprint.view_project_admin"))


@DecoratorWraps.is_logged_in
def delete_project(project_id):
    upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
    try:
        project_name = get_project_name(project_id)
        file_path = os.path.join(upload_folder, project_name)
        delete_project_row(project_id)
        #os.rmdir(file_path)
        shutil.rmtree(file_path)
        flash("Project deleted!", "success")
        return redirect(url_for("blueprint.view_all_projects"))
    except Exception as e:
        print(e)
        print(tb.format_exception(None, e, e.__traceback__))
        flash("Project could not be deleted!", "danger")
        return redirect(url_for("blueprint.view_all_projects"))


def get_paginated_projects(sort_by, town=None):
    all_projects = []
    paginated_projects = []

    search = False
    q = request.args.get('q')
    if q:
        search = True

    # setting pagination config
    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 9  # per page
    offset = page * limit - limit

    if town is None:
        try:
            all_projects, paginated_projects = get_all_projects(limit=limit, offset=offset, sort_by=sort_by)
        except Exception as e:
            print("Error with getting projects")
            print(e)
            print(tb.format_exception(None, e, e.__traceback__))
        pagination = Pagination(page=page, total=len(all_projects), search=search, record_name='projects',
                                per_page=limit, css_framework='bootstrap', alignment='center', bs_version='5')
    else:
        try:
            all_projects, paginated_projects = get_projects_by_town(town=town, limit=limit, offset=offset, sort_by=sort_by)
        except Exception as e:
            print("Error with getting projects by town")
            print(e)
            print(tb.format_exception(None, e, e.__traceback__))
        print("projects by town length: " + str(len(all_projects)))
        pagination = Pagination(page=page, total=len(all_projects), search=search, record_name='projects',
                                per_page=limit, css_framework='bootstrap', alignment='center', bs_version='5')

    return paginated_projects, pagination


def get_all_project_thumbnails(projects):
    photo_thumbnails = []

    try:
        for project in projects:
            thumbnail = get_project_thumbnail(project_id=project[0])
            first_photo_path = url_for('static', filename='Placeholder_view_vector.svg.png')
            if len(thumbnail) > 0:
                # first_photo_path = url_for('static', filename='uploads/' + project[1] + '/' + project_photos[0])
                first_photo_path = str(thumbnail).replace('\\', '/')
                # print(first_photo_path)
            photo_thumbnails.append(first_photo_path)
    except Exception as e:
        print("Error getting thumbnails")
        print(e)
        print(tb.format_exception(None, e, e.__traceback__))
    return photo_thumbnails


def get_projects(sort_by='DESC'):
    return get_all_projects(sort_by=sort_by)
