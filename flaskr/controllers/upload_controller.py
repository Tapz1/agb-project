from flask import current_app, send_from_directory
# from config.config import ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.app_context().app.config['ALLOWED_EXTENSIONS']


def download_file(name):
    return send_from_directory(current_app.app_context().app.config['UPLOAD_FOLDER'], name)

