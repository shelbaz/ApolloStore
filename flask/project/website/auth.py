

from flask import redirect, g, Blueprint, request, abort
from project import logger
from project.controllers.authentication import AuthenticationController
from flask_login import current_user, login_user, logout_user
from project.orm import Mapper
from project.website.views import website_blueprint

auth_blueprint = Blueprint('auth_blueprint', __name__)


@website_blueprint.before_request
@auth_blueprint.before_request
def before_request():
    g.user = current_user


# Registers a new client
@auth_blueprint.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    address = request.form.get('address')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    admin = False

    if first_name and last_name and address and email and password and phone and (admin is not None):

        user = AuthenticationController.create_user(first_name, last_name, address, email, password, phone, admin)

        if user:
            # logs user in after successful registration
            g.user = user
            login_user(g.user)
            return redirect('/')
        else:
            logger.error('couldnt create user')
            abort(403)


# Logs the user in
@auth_blueprint.route('/login', methods=['POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect('/dashboard')

    email = request.form.get('email')
    password = request.form.get('password')

    rows = Mapper.query('users', email=email)
    user = AuthenticationController.get_user_from_rows(rows)

    if not user or not user.verify_password(password):
        return 'Wrong credentials.'
    g.user = user

    login_user(g.user)

    logger.info(g.user.first_name + ' ' + g.user.last_name + ' (' + g.user.email + ') logged in')
    if g.user.admin:
        return redirect('/dashboard')
    return redirect('/home')



# Logs the user out
@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')
