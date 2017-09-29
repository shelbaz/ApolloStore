
from flask import g
from project import logger
from project.models import connect_to_db
from project.models.desktop_model import Desktop
from project.models.laptop_model import Laptop
from project.models.monitor_model import Monitor
from project.models.tablet_model import Tablet
from project.models.television_model import Television
from project.models.inventory_model import Inventory
from project.models.item_model import Item
from re import match
from uuid import uuid4
import traceback


#############################################################################
## The following functions create an object from the electronics types, and
## inserts it into the database.
##
## They return the object created.
#############################################################################


# Creates a desktop that is valid
def create_desktop(brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            desktop = Desktop(model=str(uuid4()), brand=brand, price=price, weight=weight, processor=processor,
                              ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, dimensions=dimensions)
            desktop.insert_into_db()

            logger.info('Desktop created successfully!')

            return desktop

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a laptop that is valid
def create_laptop(brand, price, weight, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            laptop = Laptop(model=str(uuid4()), brand=brand, price=price, weight=weight, display_size=display_size, processor=processor, ram_size=ram_size,
                            cpu_cores=cpu_cores, hd_size=hd_size, battery_info=battery_info, os=os, touchscreen=touchscreen, camera=camera)
            laptop.insert_into_db()

            logger.info('Laptop created successfully!')

            return laptop

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a tablet that is valid
def create_tablet(brand, price, weight, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            tablet = Tablet(model=str(uuid4()), brand=brand, price=price, weight=weight,display_size=display_size, dimensions=dimensions, processor=processor,
                            ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, battery=battery, os=os, camera_info=camera_info)

            tablet.insert_into_db()

            logger.info('Tablet created successfully!')

            return tablet

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a monitor that is valid
def create_monitor(brand, price, weight, dimensions):
    try:
        if validate_price(price) and validate_weight(weight):

            monitor = Monitor(model=str(uuid4()), brand=brand, price=price, weight=weight, dimensions=dimensions)
            monitor.insert_into_db()

            logger.info('Monitor created successfully!')

            return monitor

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a television that is valid
def create_television(brand, price, weight, type, dimensions):
    try:
        if validate_price(price) and validate_weight(weight):

            television = Television(model=str(uuid4()), brand=brand, price=price, weight=weight, type=type, dimensions=dimensions)
            television.insert_into_db()

            logger.info('Television created successfully!')

            return television

    except Exception as e:
        logger.error(traceback.format_exc())


#############################################################################
## The following functions query the database of a list of rows in each
## electronic type, as well as their current count in the inventory of the
## shop.
##
## They return a list of lists of the following format:
## [
##     [object1, count],
##     [object2, count],
##     ...
## ]
##
## If there is no rows in an electronic type, it returns None.
#############################################################################


# Queries the list of all desktops and their count
def get_all_desktops():
    try:
        desktops = Desktop.query_filtered_by()
        desktops_with_count = []

        if desktops:
            for desktop in desktops:
                count = get_count('desktops', desktop.model)
                desktops_with_count.append([desktop, count])
            return desktops_with_count
        else:
            return None
    except Exception as e:
        logger.error(traceback.format_exc())


# Queries the list of all laptops and their count
def get_all_laptops():
    try:
        laptops = Laptop.query_filtered_by()
        laptops_with_count = []

        if laptops:
            for laptop in laptops:
                count = get_count('laptops', laptop.model)
                laptops_with_count.append([laptop, count])
            return laptops_with_count
        else:
            return None
    except Exception as e:
        logger.error(traceback.format_exc())


# Queries the list of all tablets and their count
def get_all_tablets():
    try:
        tablets = Tablet.query_filtered_by()
        tablets_with_count = []

        if tablets:
            for tablet in tablets:
                count = get_count('tablets', tablet.model)
                tablets_with_count.append([tablet, count])
            return tablets_with_count
        else:
            return None
    except Exception as e:
        logger.error(traceback.format_exc())


# Queries the list of all monitors and their count
def get_all_monitors():
    try:
        monitors = Monitor.query_filtered_by()
        monitors_with_count = []

        if monitors:
            for monitor in monitors:
                count = get_count('monitors', monitor.model)
                monitors_with_count.append([monitor, count])
            return monitors_with_count
        else:
            return None
    except Exception as e:
        logger.error(traceback.format_exc())


# Queries the list of all televisions and their count
def get_all_televisions():
    try:
        televisions = Television.query_filtered_by()
        televisions_with_count = []

        if televisions:
            for television in televisions:
                count = get_count('televisions', television.model)
                televisions_with_count.append([television, count])
            return televisions_with_count
        else:
            return None
    except Exception as e:
        logger.error(traceback.format_exc())


#############################################################################
## All functions that deal with the inventories table should be declared
## here.
#############################################################################


# Gets count of items in inventory for a model
def get_count(electronic_type, model):
    try:
        query = 'SELECT COUNT(*) FROM inventories NATURAL JOIN (SELECT * FROM %s WHERE model=\'%s\') AS x;' % (electronic_type, model)
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()
        return count[0]
    except Exception as e:
        logger.error(traceback.format_exc())


# Adds an item of a specific model number to the inventory
def add_item_to_inventory(model):
    try:
        inventory = Inventory(id=str(uuid4()), model=model)
        inventory.insert_into_db()

        logger.info('Added %s to the inventory successfully!' % (model,))

        return inventory

    except Exception as e:
        logger.error(traceback.format_exc())


#############################################################################
## All validators should be defined here. They should return True if the
## value is valid and False if it is invalid.
#############################################################################


# Validates that a positive price is entered
def validate_price(price):
    return (float(price) > 0)


# Validates that a positive weight is entered
def validate_weight(weight):
    return (float(weight) > 0)


# Validates that the RAM size entered is a power of 2
def validate_ram_size(ram_size):
    return (int(ram_size) > 0)


def validate_cpu_cores(cpu_cores):
    return (int(cpu_cores) > 0)


# Validates that a positive hard drive disk size is entered
def validate_hd_size(hd_size):
    return (int(hd_size) > 0)
