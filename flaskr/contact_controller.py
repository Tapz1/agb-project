from flask import render_template, request, session, url_for, current_app
import os
from flaskr.upload_controller import upload_bg_image
from flaskr.submissionForms import UploadForm


def contact():
    session.modified = True
    image_form = UploadForm()

    # grab all images in contact-images folder easy to add awards later on

    img_list = []
    try:
        contact_img_dir = os.path.join(current_app.root_path, 'static', 'contact-images')

        contact_images = sorted(os.listdir(contact_img_dir))

        for img in contact_images:
            img_path = url_for('static', filename=f"contact-images/{img}")
            img_list.append(img_path)
    except Exception as e:
        print(f"Issue getting contact-images: {e}")

    if request.method == 'POST' and "upload-image" in request.form:
        upload_bg_image(page_name="contact")

    return render_template("contact.html", image_form=image_form, title="Contact Us", img_list=img_list)
