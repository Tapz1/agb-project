from flask import render_template, request, session, current_app
import os
from flaskr.upload_controller import upload_bg_image
from flaskr.submissionForms import UploadForm


def contact():
    session.modified = True
    image_form = UploadForm()

    # grab all images in contact-images folder easy to add awards later on
    contact_img_dir = current_app.app_context().app.config['CONTACT_IMAGE_DIR']
    img_list = []
    contact_images = os.listdir(contact_img_dir)

    for img in contact_images:
        print(img)
        img_path = os.path.join(contact_img_dir, img)
        img_list.append(img_path)

    if request.method == 'POST' and "upload-image" in request.form:
        upload_bg_image(page_name="contact")

    return render_template("contact.html", image_form=image_form, title="Contact Us", img_list=img_list)
