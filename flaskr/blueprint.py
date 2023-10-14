from flask import Blueprint
from flaskr.controllers.home_controller import home
from flaskr.controllers.gallery_controller import gallery
from flaskr.controllers.contact_controller import contact
from flaskr.controllers.testimonial_controller import testimonials


blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(home)
blueprint.route('/contact', methods=['GET'])(contact)
blueprint.route('/testimonials', methods=['GET'])(testimonials)
blueprint.route('/gallery', methods=['GET'])(gallery)

