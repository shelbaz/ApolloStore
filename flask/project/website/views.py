# -----------------------------------------------
# This is where all the routes are defined.
# -----------------------------------------------

from flask import render_template, Blueprint, g, request, redirect
from project.controllers.desktop import DesktopController
from project.controllers.tablet import TabletController
from project.controllers.monitor import MonitorController
from project.controllers.laptop import LaptopController
from flask_login import login_required
from project import logger
from project.controllers.inventory import InventoryController

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
        return redirect('/dashboard')
    return render_template('index.html')


@website_blueprint.route('/add-inventory/<string:electronic>/<string:model>', methods=['POST'])
@login_required
def add_desktop_inventory(electronic, model):
    InventoryController.add_item_to_inventory(model)
    return redirect('/' + electronic)


@website_blueprint.route('/remove-inventory/<string:electronic>/<string:model>', methods=['POST'])
@login_required
def delete_item_from_inventory(electronic, model):
    InventoryController.delete_item_from_inventory(model)
    return redirect('/' + electronic)


@website_blueprint.route('/desktop', methods=['GET', 'POST'])
@login_required
def desktop():
    if request.method == 'POST':
        price = request.form.get('price')
        weight = request.form.get('weight')
        brand = request.form.get('brand')
        processor = request.form.get('processor')
        ramsize = request.form.get('ram_size')
        cpucores = request.form.get('cpu_cores')
        hdsize = request.form.get('hd_size')
        dimensions = request.form.get('desktopdimensions')

        if price and weight and brand and processor and ramsize and cpucores and hdsize and dimensions:
            desktop = DesktopController.create_desktop(brand, price, weight, processor, ramsize, cpucores, hdsize, dimensions)

            if desktop:
                return redirect('/desktop')
            else:
                logger.error('couldnt create desktop item')

    return render_template('desktop.html', user=g.user, desktops=DesktopController.get_all_desktops())


@website_blueprint.route('/laptop', methods=['GET', 'POST'])
@login_required
def laptop():
    if request.method == 'POST':

        price = request.form.get('price')
        weight = request.form.get('weight')
        brand = request.form.get('brand')
        processor = request.form.get('processor')
        ramsize = request.form.get('ram_size')
        cpucores = request.form.get('cpu_cores')
        hdsize = request.form.get('hd_size')
        operatingsystem = request.form.get('operating_system')
        displaysize = request.form.get('laptop_display_size')
        touchscreen = request.form.get('touchscreen')
        camera = request.form.get('camera')
        if touchscreen:
            touchscreen = True
        else:
            touchscreen = False
        if camera:
            camera = True
        else:
            camera = False
        battery = request.form.get('battery')

        if price and weight and brand and processor and ramsize and cpucores and hdsize and displaysize:
            laptop = LaptopController.create_laptop(brand, price, weight, displaysize, processor, ramsize, cpucores, hdsize, battery, operatingsystem, touchscreen, camera)

            if laptop:
                return redirect('/laptop')
            else:
                logger.error('couldnt create laptop item')

    return render_template('laptop.html', user=g.user, laptops=LaptopController.get_all_laptops())


@website_blueprint.route('/tablet', methods=['GET', 'POST'])
@login_required
def tablet():
    if request.method == 'POST':

        price = request.form.get('price')
        weight = request.form.get('weight')
        brand = request.form.get('brand')
        processor = request.form.get('processor')
        ramsize = request.form.get('ram_size')
        cpucores = request.form.get('cpu_cores')
        hdsize = request.form.get('hd_size')
        operatingsystem = request.form.get('operating_system')
        displaysize = request.form.get('tablet_display_size')
        camera = request.form.get('camera')
        battery = request.form.get('battery')
        dimensions = request.form.get('dimensions')

        if price and weight and brand and processor and ramsize and cpucores and hdsize and displaysize:
            tablet = TabletController.create_tablet(brand, price, weight, displaysize, dimensions, processor, ramsize, cpucores, hdsize, battery, operatingsystem, camera)

            if tablet:
                return redirect('/tablet')
            else:
                logger.error('couldnt create tablet item')

    return render_template('tablet.html', user=g.user, tablets=TabletController.get_all_tablets())


@website_blueprint.route('/monitor', methods=['GET', 'POST'])
@login_required
def monitor():
    if request.method == 'POST':

        price = request.form.get('price')
        weight = request.form.get('weight')
        brand = request.form.get('brand')
        dimensions = request.form.get('monitor_dimensions')

        if price and weight and brand and dimensions:
            monitor = MonitorController.create_monitor(brand, price, weight, dimensions)

            if monitor:
                return redirect('/monitor')
            else:
                logger.error('couldnt create monitor item')

    return render_template('monitor.html', user=g.user, monitors=MonitorController.get_all_monitors())


@website_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=g.user)
