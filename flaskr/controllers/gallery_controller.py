import os
import traceback

from flask import render_template, flash, url_for, request, session, current_app

from flaskr.controllers.project_controller import get_paginated_projects, get_all_project_thumbnails
from flaskr.controllers.project_controller import get_multiple_project_items
from flaskr.controllers.image_controller import get_checked_images
from flaskr.controllers.upload_controller import upload_bg_image
from flaskr.models.submissionForms import GalleryDropdowns, UploadForm
import traceback as tb


def gallery():
    session.modified = True
    image_form = UploadForm()

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
        images = get_checked_images()
        if len(images) > 0:
            first_photo = images[0]  # to add first photo as active on carousel
            # latest_photo = "uploads/" + max(glob.glob(upload_folder))
            enumerated_photos = [*range(0, len(images))]  # for carousel indicators
            # print(enumerated_photos)

    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))

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
        get_towns = get_multiple_project_items("town")
        for town in get_towns:
            towns.append(town[0])
        dropdown_form.filter_by.choices = towns

    except Exception as e:
        flash("Unable to get towns", 'danger')
        print(e)

    if request.method == 'POST':

        if "filter_by" in request.form:
            # sort_by = request.form['sort_by']
            # dropdown_form.sort_by.data = sort_by
            town = request.form['filter_by']
            if town == 'All':
                try:
                    # projects
                    """pagination"""
                    projects, pagination = get_paginated_projects(sort_by="desc")
                    project_thumbnails = get_all_project_thumbnails(projects)
                    #redirect(url_for("blueprint.gallery"))
                except Exception as e:
                    flash("Unable to get all projects", 'danger')
                    print(e)
            else:
                try:
                    projects, pagination = get_paginated_projects(town=town, sort_by="desc")
                    project_thumbnails = get_all_project_thumbnails(projects)
                    with current_app.app_context().app.test_request_context():
                        print(url_for("blueprint.gallery", page=''))

                    dropdown_form.filter_by.data = town     # FINALLY figured this out - to set the dropdown value on the frontend to what's selected, set form data to that value DUH
                    #redirect(url_for("blueprint.gallery", page='1'))

                except Exception as e:
                    flash("Unable to get town-specific projects", 'danger')
                    print(e)

        if "upload-image" in request.form:
            upload_bg_image(page_name="gallery")

    return render_template("gallery.html", images=images, form=dropdown_form, image_form=image_form,
                           enumerated_photos=enumerated_photos, first_photo=first_photo,
                           project_data=zip(projects, project_thumbnails), pagination=pagination)


def view_gallery_carousel():
    session.modified = True
    image_form = UploadForm()

    upload_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], "gallery_carousel")
    photos = []

    try:
        photos = os.listdir(upload_folder)
        photo_names = [photo for photo in photos]
        photos = ['uploads/gallery_carousel' + photo for photo in photos]

        return render_template("gallery_carousel_photos.html", all_photos=zip(photos, photo_names))


    except Exception as e:
        print("Error with getting images:")
        print(e)
        print(traceback.format_exception(None, e, e.__traceback__))

