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
import json

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
        if g.user.admin:
            return redirect('/dashboard')
        return redirect('/home')
    return render_template('index.html')


@website_blueprint.route('/add-inventory/<string:electronic>/<string:model>', methods=['POST'])
@login_required
def add_desktop_inventory(electronic, model):
    if g.user.admin:
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
    if g.user.admin:
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

@website_blueprint.route('/desktop-client', methods=['GET', 'POST'])
@login_required
def desktop_client():
    desktops=DesktopController.get_all_desktops()
    
    # do all the group by for the filter selects here
    # filters -> brand, processor, ram_size, cpu_core
    filters = {
        'brand': [],
        'processor': [],
        'ram_size': [],
        'cpu_cores': []
    }

    for desktop in desktops:
        if desktop[0]['brand'] not in filters['brand']: 
            filters['brand'].append(desktop[0]['brand'])

        if desktop[0]['processor'] not in filters['processor']: 
            filters['processor'].append(desktop[0]['processor'])

        if desktop[0]['ram_size'] not in filters['ram_size']: 
            filters['ram_size'].append(desktop[0]['ram_size'])

        if desktop[0]['cpu_cores'] not in filters['cpu_cores']: 
            filters['cpu_cores'].append(desktop[0]['cpu_cores'])
        

    logger.info(filters)
    return render_template('desktop-client.html', user=g.user, filters=filters)

@website_blueprint.route('/desktop-client/table', methods=['GET'])
def desktop_client_table():    
    return json.dumps({
        'data': DesktopController.get_all_desktops(request.args.to_dict())
    })

@website_blueprint.route('/desktop-client/<string:attr>', methods=['GET', 'POST'])
@login_required
def desktop_client_order(attr):
    return render_template('desktop-client.html', user=g.user, desktops=DesktopController.get_all_desktops_order(attr))

@website_blueprint.route('/edit-desktop', methods=['POST'])
@login_required
def edit_desktop():
    if g.user.admin:
        model = request.form.get('model')
        price = request.form.get('price')
        weight = request.form.get('weight')
        brand = request.form.get('brand')
        processor = request.form.get('processor')
        ramsize = request.form.get('ram_size')
        cpucores = request.form.get('cpu_cores')
        hdsize = request.form.get('hd_size')
        dimensions = request.form.get('desktopdimensions')

        if model and price and weight and brand and processor and ramsize and cpucores and hdsize and dimensions:
            desktop = DesktopController.update_desktop(model, brand=brand, price=price, weight=weight, processor=processor, ram_size=ramsize, cpu_cores=cpucores, hd_size=hdsize, dimensions=dimensions)
            if desktop:
                return redirect('/desktop')
            else:
                logger.error('could not update desktop item')

        # return render_template('desktop.html', user=g.user, desktops=DesktopController.get_all_desktops())


@website_blueprint.route('/laptop', methods=['GET', 'POST'])
@login_required
def laptop():
    if g.user.admin:
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

@website_blueprint.route('/laptop-client', methods=['GET', 'POST'])
@login_required
def laptop_client():
    return render_template('laptop-client.html', user=g.user, laptops=LaptopController.get_all_laptops())



@website_blueprint.route('/edit-laptop', methods=['POST'])
@login_required
def edit_laptop():
    if g.user.admin:
        model = request.form.get('model')
        price = request.form.get('price')
        weight = request.form.get('weight')
        brand = request.form.get('brand')
        displaysize = request.form.get('laptop_display_size')
        processor = request.form.get('processor')
        ramsize = request.form.get('ram_size')
        cpucores = request.form.get('cpu_cores')
        hdsize = request.form.get('hd_size')
        battery = request.form.get('battery_info')
        operatingsystem = request.form.get('operating_system')
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

        if model and price and weight and brand and processor and ramsize and cpucores and hdsize and displaysize:
            laptop = LaptopController.update_laptop(model, brand=brand, price=price, weight=weight, display_size =displaysize,
                                                    processor=processor, ram_size=ramsize, cpu_cores=cpucores, hd_size=hdsize,
                                                    battery_info=battery, os=operatingsystem, touchscreen=touchscreen,
                                                    camera=camera)

            if laptop:
                return redirect('/laptop')
            else:
                logger.error('could not update laptop item')



@website_blueprint.route('/tablet', methods=['GET', 'POST'])
@login_required
def tablet():
    if g.user.admin:
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


@website_blueprint.route('/tablet-client', methods=['GET', 'POST'])
@login_required
def tablet_client():
    return render_template('tablet-client.html', user=g.user, tablets=TabletController.get_all_tablets())


@website_blueprint.route('/edit-tablet', methods=['POST'])
@login_required
def edit_tablet():
    if g.user.admin:
        model = request.form.get('model')
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

        if model and price and weight and brand and processor and ramsize and cpucores and hdsize and displaysize:
            tablet = TabletController.update_tablet(model, brand=brand , price=price, weight=weight, display_size=displaysize,
                                                    dimensions=dimensions, processor=processor, ram_size=ramsize,
                                                    cpu_cores=cpucores, hd_size=hdsize, battery=battery, os=operatingsystem,
                                                    camera_info=camera)
            if tablet:
                return redirect('/tablet')
            else:
                logger.error('couldnt create tablet item')


@website_blueprint.route('/monitor', methods=['GET', 'POST'])
@login_required
def monitor():
    if g.user.admin:
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


@website_blueprint.route('/monitor-client', methods=['GET', 'POST'])
@login_required
def monitor_client():
    return render_template('monitor-client.html', user=g.user, monitors=MonitorController.get_all_monitors())

@website_blueprint.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    return render_template('cart.html', user=g.user)


@website_blueprint.route('/edit-monitor', methods=['POST'])
@login_required
def edit_monitor():
    if g.user.admin:
        model = request.form.get('model')
        price = request.form.get('price')
        weight = request.form.get('weight')
        brand = request.form.get('brand')
        dimensions = request.form.get('monitor_dimensions')
        if model and price and weight and brand and dimensions:
            monitor = MonitorController.update_monitor(model, brand=brand, price=price, weight=weight, dimensions=dimensions)
            if monitor:
                return redirect('/monitor')
            else:
                logger.error('couldnt create monitor item')



@website_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if g.user.admin:
        return render_template('dashboard.html', user=g.user)


@website_blueprint.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=g.user)
