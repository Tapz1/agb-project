from flask import Blueprint
from flaskr.controllers.home_controller import home
from flaskr.controllers.gallery_controller import gallery
from flaskr.controllers.contact_controller import contact
from flaskr.controllers.testimonial_controller import testimonials, testimonial_form
from flaskr.controllers.login_controller import login, logout
from flaskr.controllers.admin_controller import admin_portal, approve_testimonial, delete_testimonial, delete_testimonial_request
from flaskr.controllers.image_controller import view_images, delete_image



blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(home)
blueprint.route('/contact', methods=['GET'])(contact)
blueprint.route('/testimonials', methods=['GET'])(testimonials)
blueprint.route('/gallery', methods=['GET'])(gallery)
blueprint.route('/login', methods=['GET', 'POST'])(login)
blueprint.route('/logout', methods=['GET', 'POST'])(logout)
blueprint.route('/admin', methods=['GET', 'POST'])(admin_portal)
blueprint.route('/testimonial-form/<token>', methods=['GET', 'POST'])(testimonial_form)
blueprint.route('/admin/approve-testimonial/<string:testimonial_id>', methods=['POST'])(approve_testimonial)
blueprint.route('/admin/delete-testimonial-request/<string:testimonial_id>', methods=['POST'])(delete_testimonial_request)
blueprint.route('/admin/delete-testimonial/<string:testimonial_id>', methods=['POST'])(delete_testimonial)
blueprint.route('/admin/view-images', methods=['GET', 'POST'])(view_images)
blueprint.route('/admin/delete-image/<string:filename>', methods=['POST'])(delete_image)

