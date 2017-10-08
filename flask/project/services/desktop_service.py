
from flask import g
from project import logger
from project.models import connect_to_db
from project.models.desktop_model import Desktop
from project.gateaways.desktop_gateaway import DesktopGateaway
from project.gateaways.item_gateaway import ItemGateaway
from project.models.item_model import Item
from project.services.electronics import validate_price, validate_weight, validate_ram_size, validate_cpu_cores, validate_hd_size, get_count
from re import match
from uuid import uuid4
import traceback

# Creates a desktop that is valid
def create_desktop(brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            desktop = Desktop(model=str(uuid4()), brand=brand, price=price, weight=weight, processor=processor,
                              ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, dimensions=dimensions)
            ItemGateaway.insert_into_db(desktop)
            DesktopGateaway.insert_into_db(desktop)

            logger.info('Desktop created successfully!')

            return desktop

    except Exception as e:
        logger.error(traceback.format_exc())

# Queries the list of all desktops and their count
def get_all_desktops():
    try:
        rows = DesktopGateaway.query_filtered_by()
        desktops = get_desktops_from_rows(rows)
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

# Returns all desktops from rows taken from db
def get_desktops_from_rows(rows):
    if rows:
        desktops=[]
        for row in rows:
            desktop = Desktop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            desktops.append(desktop)
        if desktops:
            return desktops
        else:
            return None
    else:
        return None
