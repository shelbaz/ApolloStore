
from flask import g
from flask_httpauth import HTTPBasicAuth
from project import logger
from project.models.desktop_model import Desktop
from project.models.laptop_model import Laptop
from project.models.monitor_model import Monitor
from project.models.tablet_model import Tablet
from project.models.television_model import Television
from re import match
from uuid import uuid4
import traceback

auth = HTTPBasicAuth()


# Creates a desktop that is valid
def create_desktop(price, weight, brand, processor, ram_size, cpu_cores, hd_size, dimensions):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            desktop = Desktop(model=str(uuid4()), price=price, weight=weight, brand=brand, processor=processor,
                              ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, dimensions=dimensions)
            desktop.insert_into_db()

            logger.info('Desktop created successfully!')

            return desktop

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a laptop that is valid
def create_laptop(price, weight, brand, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            laptop = Laptop(model=str(uuid4()), price=price, weight=weight, brand=brand, display_size=display_size, processor=processor, ram_size=ram_size,
                            cpu_cores=cpu_cores, hd_size=hd_size, battery_info=battery_info, os=os, touchscreen=touchscreen, camera=camera)
            laptop.insert_into_db()

            logger.info('Laptop created successfully!')

            return laptop

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a tablet that is valid
def create_tablet(price, weight, brand, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            tablet = Tablet(model=str(uuid4()), price=price, weight=weight, brand=brand, display_size=display_size, dimensions=dimensions, processor=processor,
                            ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, battery=battery, os=os, camera_info=camera_info)
            tablet.insert_into_db()

            logger.info('Tablet created successfully!')

            return tablet

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a monitor that is valid
def create_monitor(price, weight, brand, dimensions):
    try:
        if validate_price(price) and validate_weight(weight):

            monitor = Monitor(model=str(uuid4()), price=price, weight=weight, brand=brand, dimensions=dimensions)
            monitor.insert_into_db()

            logger.info('Monitor created successfully!')

            return monitor

    except Exception as e:
        logger.error(traceback.format_exc())


# Creates a television that is valid
def create_television(price, weight, brand, type, dimensions):
    try:
        if validate_price(price) and validate_weight(weight):

            television = Television(model=str(uuid4()), price=price, weight=weight, brand=brand, type=type, dimensions=dimensions)
            television.insert_into_db()

            logger.info('Television created successfully!')

            return television

    except Exception as e:
        logger.error(traceback.format_exc())


def validate_price(price):
    return (price > 0)


def validate_weight(weight):
    return (weight > 0)

# validates that ram_size is a power of 2
def validate_ram_size(ram_size):
    return (ram_size != 0 and ((ram_size & (ram_size - 1)) == 0))


def validate_cpu_cores(cpu_cores):
    return (cpu_cores == 2 or cpu_cores == 4)


def validate_hd_size(hd_size):
    return (hd_size > 0)
