from flask import Blueprint
from flaskr.home_controller import home
from flaskr.gallery_controller import gallery
from flaskr.contact_controller import contact
from flaskr.testimonial_controller import testimonials, testimonial_form
from flaskr.login_controller import login, logout
from flaskr.admin_controller import admin_portal, approve_testimonial, delete_testimonial, delete_testimonial_request
from flaskr.image_controller import view_images, delete_image, view_project



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
blueprint.route('/admin/view-project/<string:project_name>', methods=['GET', 'POST'])(view_project)
blueprint.route('/admin/delete-image/<string:project_name>/<string:filename>', methods=['POST'])(delete_image)

