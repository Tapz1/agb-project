import os
from flask import render_template, redirect, flash, url_for, request, session, current_app


def gallery():
    session.modified = True
    photos = []
    first_photo = None
    enumerated_photos = []
    # preview slideshow banner
    try:
        folder_name = ''
        # image_folder = os.path.join(current_app.app_context().app.config['UPLOAD_FOLDER'], f'{folder_name}')  # path for prod
        # image_folder = os.path.join('flaskr/static/uploads', f'{folder_name}')  # path for dev
        image_folder = current_app.app_context().app.config['UPLOAD_FOLDER']
        photos = os.listdir(image_folder)
        formatted_name = f"uploads/{folder_name}/"
        photos = [formatted_name + photo for photo in photos]
        if len(photos) > 0:
            first_photo = photos[0]
            enumerated_photos = [*range(0, len(photos))]  # for carousel indicators
    except Exception as e:
        print(e)

    return render_template("gallery.html", photos=photos, enumerated_photos=enumerated_photos, first_photo=first_photo)
