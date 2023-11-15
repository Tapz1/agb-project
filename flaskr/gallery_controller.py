import os
from flask import render_template, redirect, flash, url_for, request, session, current_app

from flaskr.project_controller import get_paginated_projects, get_all_project_thumbnails
from flaskr.project_service import get_project_towns
from flaskr.image_controller import get_limited_images
from flaskr.submissionForms import GalleryDropdowns
import traceback as tb


def gallery():
    session.modified = True

    images = []
    first_photo = None
    enumerated_photos = []

    dropdown_form = GalleryDropdowns()
    projects = []
    project_thumbnails = []
    pagination = None
    towns = ["All"]
    #town = dropdown_form.filter_by.data


    # preview slideshow banner
    try:
        folder_name = ''
        # image_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], f'{folder_name}')  # path for prod
        # image_folder = os.path.join('flaskr/static/uploads', f'{folder_name}')  # path for dev
        upload_folder = current_app.app_context().app.config['UPLOAD_FOLDER']

        images = get_limited_images(5)

        if len(images) > 0:
            first_photo = images[0]
            enumerated_photos = [*range(0, len(images))]  # for carousel indicators
        print(f"photos len: {len(images)}")

    except Exception as e:
        flash("Unable to get images", 'danger')
        print(e)

    try:
        projects, pagination = get_paginated_projects(sort_by='DESC')

        # projects & thumbnails binding
        project_thumbnails = get_all_project_thumbnails(projects)


    except Exception as e:
        print(e)
        print(tb.format_exception(None, e, e.__traceback__))
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
        sort_by = request.form['sort_by']
        dropdown_form.sort_by.data = sort_by
        town = request.form['filter_by']

        #town = dropdown_form.filter_by.data
        if town == 'All':
            try:
                # projects
                """pagination"""
                projects, pagination = get_paginated_projects(sort_by=sort_by)
                project_thumbnails = get_all_project_thumbnails(projects)
                #redirect(url_for("blueprint.gallery"))
            except Exception as e:
                flash("Unable to get all projects", 'danger')
                print(e)
        else:
            try:
                projects, pagination = get_paginated_projects(town=town, sort_by=sort_by)
                project_thumbnails = get_all_project_thumbnails(projects)
                with current_app.app_context().app.test_request_context():
                    print(url_for("blueprint.gallery", page=''))

                dropdown_form.filter_by.data = town     # FINALLY figured this out - to set the dropdown value on the frontend to what's selected, set form data to that value DUH
                #redirect(url_for("blueprint.gallery", page='1'))

            except Exception as e:
                flash("Unable to get town-specific projects", 'danger')
                print(e)

    return render_template("gallery.html", images=images, form=dropdown_form,
                           enumerated_photos=enumerated_photos, first_photo=first_photo,
                           project_data=zip(projects, project_thumbnails), pagination=pagination)




