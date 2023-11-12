# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from datetime import timedelta
from flask import Flask
from flaskr.config import (UPLOAD_FOLDER, DB_NAME, SECRET_KEY, SECURITY_PASSWORD_SALT, EMAIL_USERNAME,
                           EMAIL_PASSWORD, EMAIL_SEND_AS, TO_EMAIL, DEV_EMAIL, CLIENT_EMAIL, ADMIN_PASSWORD, ALLOWED_EXTENSIONS,
                           PATH_SLICE)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        SECURITY_PASSWORD_SALT=SECURITY_PASSWORD_SALT,
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        PATH_SLICE=PATH_SLICE,
        ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS,
        # DATABASE=os.path.join(flaskr.instance_path, 'flaskr.sqlite'),
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        DATABASE=os.path.join(app.instance_path, DB_NAME),
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_DEBUG=True,
        MAIL_USERNAME=EMAIL_USERNAME,
        MAIL_PASSWORD=EMAIL_PASSWORD,
        # TO_EMAIL = os.environ.get('BC_EMAIL'),
        TO_EMAIL=TO_EMAIL,
        MAIL_DEFAULT_SENDER=EMAIL_SEND_AS,
        MAIL_MAX_EMAILS=None,
        MAIL_ASCII_ATTACHMENTS=False,
        DEV_EMAIL=DEV_EMAIL,
        CLIENT_EMAIL=CLIENT_EMAIL,
        ADMIN_PASSWORD=ADMIN_PASSWORD
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    from flaskr.blueprint import blueprint
    app.register_blueprint(blueprint, url_prefix='/')

    from flaskr import db
    db.init_app(app)

    app.permanent_session_lifetime = timedelta(hours=4)

    return app


app = create_app()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, port=5002)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
