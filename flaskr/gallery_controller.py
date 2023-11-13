import os
from flask import render_template, redirect, flash, url_for, request, session, current_app

from flaskr.project_controller import get_paginated_projects
from flaskr.project_service import get_project_towns
from flaskr.image_service import get_limited_images
from flaskr.submissionForms import GalleryDropdowns


def gallery(town):
    session.modified = True

    images = []
    first_photo = None
    enumerated_photos = []

    dropdown_form = GalleryDropdowns()
    projects = []
    photo_thumbnails = []
    pagination = None
    towns = ["All"]
    #town = dropdown_form.filter_by.data


    # preview slideshow banner
    try:
        folder_name = ''
        # image_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], f'{folder_name}')  # path for prod
        # image_folder = os.path.join('flaskr/static/uploads', f'{folder_name}')  # path for dev
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']

        images = get_limited_images()

        if len(images) > 0:
            first_photo = images[0]
            enumerated_photos = [*range(0, len(images))]  # for carousel indicators
        print(f"photos len: {len(images)}")

    except Exception as e:
        flash("Unable to get images", 'danger')
        print(e)

    try:
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']

        if town == 'All':
            projects, pagination = get_paginated_projects()
        else:
            projects, pagination = get_paginated_projects(town=town)
            pagination.page = 1
            dropdown_form.filter_by.data = town

        # projects & thumbnails binding

        for project in projects:
            project_photos = os.listdir(os.path.join(upload_folder, project[1]))
            first_photo_path = url_for('static', filename='Placeholder_view_vector.svg.png')
            if len(project_photos) > 0:
                #print("project_photos[0]: " + project_photos[0])
                first_photo_path = url_for('static', filename='uploads/' + project[1] + '/' + project_photos[0])
            #print("first_photo_path: " + first_photo_path)
            photo_thumbnails.append(first_photo_path)

        sort_dropdown = dropdown_form.sort_by.data

        #towns = get_project_towns()
        #dropdown_form.filter_by.choices = [(town[0], town[0]) for town in towns]

    except Exception as e:
        print(e)
        flash("Unable to get binded projects & thumbnails", 'danger')

    try:
        """town filtering"""
        get_towns = get_project_towns()
        for town in get_towns:
            towns.append(town[0])
        dropdown_form.filter_by.choices = towns

    except Exception as e:
        flash("Unable to get towns", 'danger')
        print(e)

    if request.method == 'POST':
        #if "filter" in request.form:

        town = request.form['filter_by']
        #town = dropdown_form.filter_by.data
        if town == 'All':
            try:
                # projects
                """pagination"""
                projects, pagination = get_paginated_projects()
                redirect(url_for("blueprint.gallery"))
            except Exception as e:
                flash("Unable to get all projects", 'danger')
                print(e)
        else:
            try:
                projects, pagination = get_paginated_projects(town=town)
                page = request.args.get('page', 1, type=int)
                pagination.page = page
                dropdown_form.filter_by.data = town     # FINALLY figured this out - to set the dropdown value on the frontend to what's selected, set form data to that value DUH
                redirect(url_for("blueprint.gallery", town=town))

            except Exception as e:
                flash("Unable to get town-specific projects", 'danger')
                print(e)

    return render_template("gallery.html", images=images, form=dropdown_form,
                           enumerated_photos=enumerated_photos, first_photo=first_photo, town=town,
                           project_data=zip(projects, photo_thumbnails), pagination=pagination)


def selected_town(town):
    return town

