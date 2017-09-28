# -----------------------------------------------
# This is where all the routes are defined.
# -----------------------------------------------

from flask import jsonify, render_template, Blueprint, g, request, abort, redirect
from project.services.authentication import create_user
from project import logger
from project.models.auth_model import User
from flask_login import login_required, current_user, login_user, logout_user

website_blueprint = Blueprint('website_blueprint', __name__)


# Endpoints are defined defined by applying a decorator on a function.
# The '/' route points to the root of the website.
# The return value of this function specifies what is returned when
# an HTTP request is made at this endpoint. In this case, Flask renders
# the template called 'index.html', which is located in the following
# location by default: flask/project/templates/
@website_blueprint.route('/')
def index():

    is_authenticated = False;

    if g.user is not None and g.user.is_authenticated:
        is_authenticated = True;
    return render_template('index.html', is_authenticated = is_authenticated)


# Temporary route to test if token authentication works
@website_blueprint.route('/test')
@login_required
def test():
    return render_template('test.html')


# Registers a new user
@website_blueprint.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    address = request.form.get('address')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    # admin = request.form.get('admin')
    admin = True

    if first_name and last_name and address and email and password and phone and (admin is not None):

        user = create_user(first_name, last_name, address, email, password, phone, admin)

        if user:
            # logs user in after successful registration
            return render_template('index.html', is_authenticated = False), 201
        else:
            logger.error("couldnt create user")
            abort(403)


# Logs the user in
@website_blueprint.route('/login', methods=['POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect('/test')

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query_filtered_by(email=email)
    if not user or not user[0].verify_password(password):
        return 'Wrong credentials.'
    g.user = user[0]

    login_user(g.user)

    logger.info(g.user.first_name + ' ' + g.user.last_name + ' (' + g.user.email + ') logged in')

    return redirect('/')


# Logs the user out
@website_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@website_blueprint.before_request
def before_request():
    g.user = current_user
