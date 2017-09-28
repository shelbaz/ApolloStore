# -----------------------------------------------
# This is where all the routes are defined.
# -----------------------------------------------

from flask import jsonify, render_template, Blueprint, g, request, abort, redirect
from project.services.authentication import create_user
from project.services.electronics import create_desktop, create_television, create_tablet, create_monitor, create_laptop
from project import logger
from project.models.auth_model import User
from flask_login import login_required, current_user, login_user, logout_user
from project.services.database_queries import get_all_users, get_all_items

website_blueprint = Blueprint('website_blueprint', __name__)


# Endpoints are defined defined by applying a decorator on a function.
# The '/' route points to the root of the website.
# The return value of this function specifies what is returned when
# an HTTP request is made at this endpoint. In this case, Flask renders
# the template called 'index.html', which is located in the following
# location by default: flask/project/templates/
@website_blueprint.route('/')
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect('/test')
    return render_template('index.html')


# Temporary route to test if token authentication works
@website_blueprint.route('/test')
@login_required
def test():
    return render_template('test.html')


@website_blueprint.route('/dashboard', methods=["GET", "POST"])
#@auth.login_required
def dashboard():
    if request.method == "POST" and request.form['desktopdimensions']:
        price = request.form['price']
        weight = request.form['weight']
        brand = request.form['brand']
        processor = request.form['processor']
        ramsize = request.form['ram_size']
        cpucores = request.form['cpu_cores']
        hdsize = request.form['hd_size']
        dimensions = request.form['desktopdimensions']

        if price and weight and brand and processor and ramsize and cpucores and hdsize and dimensions:
            desktop = create_desktop(brand, price, weight, processor, ramsize, cpucores, hdsize, dimensions)

            if desktop:
                return render_template('dashboard.html'), 201
            else:
                logger.error('couldnt create desktop item')

    if request.method == "POST" and request.form['laptop_display_size']:

        price = request.form['price']
        weight = request.form['weight']
        brand = request.form['brand']
        processor = request.form['processor']
        ramsize = request.form['ram_size']
        cpucores = request.form['cpu_cores']
        hdsize = request.form['hd_size']
        operatingsystem = request.form['operating_system']
        displaysize = request.form['laptop_display_size']
        touchscreen = request.form['touchscreen']
        camera = request.form['camera']
        battery = request.form['battery']

        if price and weight and brand and processor and ramsize and cpucores and hdsize and displaysize:
            laptop = create_laptop(brand, price, weight, displaysize, processor, ramsize, cpucores, hdsize, battery, operatingsystem, touchscreen, camera)

            if laptop:
                return render_template('dashboard.html'), 201
            else:
                logger.error('couldnt create laptop item')

    if request.method == "POST" and request.form['tablet_display_size']:

        price = request.form['price']
        weight = request.form['weight']
        brand = request.form['brand']
        processor = request.form['processor']
        ramsize = request.form['ram_size']
        cpucores = request.form['cpu_cores']
        hdsize = request.form['hd_size']
        operatingsystem = request.form['operating_system']
        displaysize = request.form['tablet_display_size']
        camera = request.form['camera']
        battery = request.form['battery']
        dimensions = request.form['dimensions']

        if price and weight and brand and processor and ramsize and cpucores and hdsize and displaysize:
            tablet = create_tablet(brand, price, weight, displaysize, dimensions, processor, ramsize, cpucores, hdsize, battery, os, camera)

            if tablet:
                return render_template('dashboard.html'), 201
            else:
                logger.error('couldnt create tablet item')

    if request.method == "POST" and request.form['monitor_dimensions']:

        price = request.form['price']
        weight = request.form['weight']
        brand = request.form['brand']
        dimensions = request.form['monitor_dimensions']

        if price and weight and brand and dimensions:
            monitor = create_monitor(brand, price, weight, dimensions)

            if monitor:
                return render_template('dashboard.html'), 201
            else:
                logger.error('couldnt create monitor item')

    if request.method == "POST" and request.form['tv_dimensions']:

        price = request.form['price']
        weight = request.form['weight']
        brand = request.form['brand']
        dimensions = request.form['tv_dimensions']
        tvtype = request.form['tv_type']

        if price and weight and brand and dimensions:
            television = create_television(brand, price, weight, tvtype, dimensions)

            if television:
                return render_template('dashboard.html'), 201
            else:
                logger.error('couldnt create tv item')

    return render_template('dashboard.html', users=get_all_users(), items=get_all_items())


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
            return render_template('index.html'), 201
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

    return redirect('/test')


# Logs the user out
@website_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@website_blueprint.before_request
def before_request():
    g.user = current_user