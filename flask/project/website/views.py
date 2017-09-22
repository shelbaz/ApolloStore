# -----------------------------------------------
# This is where all the routes are defined.
# -----------------------------------------------


from flask import jsonify, render_template, Blueprint, g, request, abort
from project.services.authentication import create_user, auth
from project import logger


website_blueprint = Blueprint('website_blueprint', __name__)


# Endpoints are defined defined by applying a decorator on a function.
# The '/' route points to the root of the website.
# The return value of this function specifies what is returned when
# an HTTP request is made at this endpoint. In this case, Flask renders
# the template called 'index.html', which is located in the following
# location by default: flask/project/templates/
@website_blueprint.route('/')
def index():
    logger.error('sup1')
    return render_template('index.html')

# Registers a new user
@website_blueprint.route('/register', methods=['POST'])
def register():
    logger.error(request.form)
    logger.error(request.form['firstNameInput'])
    abort(410)
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    address = request.form.get('address')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone') 
    # admin = request.form.get('admin')
    admin = True
    if first_name and last_name and address and email and password and phone and (admin is not None):

        user = create_user(first_name, last_name, address, email, password, phone, admin)

        if user:
            return render_template('index.html'), 201
        else:
            abort(403)


# Generates auth token if credentials are valid
@website_blueprint.route('/login')
@auth.login_required
def get_auth_token():

    token = g.user.generate_auth_token()

    logger.info(g.user.first_name + ' ' + g.user.last_name + ' (' + g.user.email + ') logged in')

    return jsonify({'token': token.decode('ascii')}), 201
