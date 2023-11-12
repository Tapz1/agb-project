from flask import Blueprint
from flaskr.home_controller import home
from flaskr.gallery_controller import gallery
from flaskr.contact_controller import contact
from flaskr.testimonial_controller import testimonials, testimonial_form
from flaskr.login_controller import login, logout
from flaskr.admin_controller import admin_portal, approve_testimonial, delete_testimonial, delete_testimonial_request
from flaskr.project_controller import view_all_projects, view_project, delete_project
from flaskr.image_controller import delete_image


blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(home)
blueprint.route('/contact', methods=['GET'])(contact)
blueprint.route('/testimonials', methods=['GET'])(testimonials)
blueprint.route('/gallery', methods=['GET', 'POST'])(gallery)
blueprint.route('/login', methods=['GET', 'POST'])(login)
blueprint.route('/logout', methods=['GET', 'POST'])(logout)
blueprint.route('/admin', methods=['GET', 'POST'])(admin_portal)
blueprint.route('/testimonial-form/<token>', methods=['GET', 'POST'])(testimonial_form)
blueprint.route('/admin/approve-testimonial/<string:testimonial_id>', methods=['POST'])(approve_testimonial)
blueprint.route('/admin/delete-testimonial-request/<string:testimonial_id>', methods=['POST'])(delete_testimonial_request)
blueprint.route('/admin/delete-testimonial/<string:testimonial_id>', methods=['POST'])(delete_testimonial)
blueprint.route('/admin/view-projects', methods=['GET', 'POST'])(view_all_projects)
blueprint.route('/admin/view-project/<string:project_id>', methods=['GET', 'POST'])(view_project)
blueprint.route('/admin/delete-project/<string:project_id>', methods=['POST'])(delete_project)
blueprint.route('/admin/delete-image/<string:image_id>/<string:project_id>/<string:filename>', methods=['POST'])(delete_image)

