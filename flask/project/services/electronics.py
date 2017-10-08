
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
