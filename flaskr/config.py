import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "database.db"

# Upload Info ###
UPLOAD_FOLDER = './static/uploads'         # path for production
#UPLOAD_FOLDER = 'flaskr/static/uploads'     # path for dev
STATIC_PATH = './static'     # path for dev
#STATIC_PATH = 'flaskr/static'     # path for dev
PATH_SLICE = 6
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# secret keys
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

# email config
#TO_EMAIL = os.environ.get('CLIENT_EMAIL')
TO_EMAIL = os.environ.get('DEV_EMAIL')    # for development ###
EMAIL_USERNAME = os.environ.get('MAILING_USERNAME')
EMAIL_PASSWORD = os.environ.get('MAILING_PASSWORD')
EMAIL_SEND_AS = EMAIL_USERNAME

# login info
CLIENT_EMAIL = os.environ.get('CLIENT_EMAIL')
DEV_EMAIL = os.environ.get('DEV_EMAIL')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
#ADMIN_PASSWORD = "test"                   # for development ###
