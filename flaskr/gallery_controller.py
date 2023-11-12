import os
from flask import render_template, redirect, flash, url_for, request, session, current_app

from flaskr.project_controller import get_paginated_projects
from flaskr.project_service import get_paginated_projects_db, get_project_towns
from flaskr.image_service import get_all_images
from flaskr.submissionForms import GalleryDropdowns



def gallery(selected_town=None):
    session.modified = True

    images = []
    first_photo = None
    enumerated_photos = []

    dropdown_form = GalleryDropdowns(filter_by=selected_town)
    projects = []
    photo_thumbnails = []
    paginated_data = None
    pagination = None
    towns = ["All"]
    town = dropdown_form.filter_by.data


    # preview slideshow banner
    try:
        folder_name = ''
        # image_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], f'{folder_name}')  # path for prod
        # image_folder = os.path.join('flaskr/static/uploads', f'{folder_name}')  # path for dev
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']

        images = get_all_images()

        if len(images) > 0:
            first_photo = images[0]
            enumerated_photos = [*range(0, len(images))]  # for carousel indicators
        print(f"photos len: {len(images)}")

    except Exception as e:
        flash("Unable to get images", 'danger')
        print(e)

    try:
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']

        if selected_town is None:
            projects, pagination = get_paginated_projects()

        # projects & thumbnails binding

        for project in projects:
            project_photos = os.listdir(os.path.join(upload_folder, project[1]))
            first_photo_path = url_for('static', filename='Placeholder_view_vector.svg.png')
            if len(project_photos) > 0:
                print("project_photos[0]: " + project_photos[0])
                first_photo_path = url_for('static', filename='uploads/' + project[1] + '/' + project_photos[0])
            print("first_photo_path: " + first_photo_path)
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
                redirect(url_for("blueprint.gallery", selected_town='All'))
            except Exception as e:
                flash("Unable to get all projects", 'danger')
                print(e)
        else:
            try:
                projects, pagination = get_paginated_projects(town=town)
                redirect(url_for("blueprint.gallery", selected_town=town))

            except Exception as e:
                flash("Unable to get town-specific projects", 'danger')
                print(e)

    return render_template("gallery.html", images=images, form=dropdown_form, projects=paginated_data,
                           enumerated_photos=enumerated_photos, first_photo=first_photo, town=town,
                           project_data=zip(projects, photo_thumbnails), pagination=pagination)




