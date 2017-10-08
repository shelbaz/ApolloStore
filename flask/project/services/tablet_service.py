
from flask import g
from project import logger
from project.models import connect_to_db
from project.models.tablet_model import Tablet
from project.gateaways.tablet_gateaway import TabletGateaway
from project.gateaways.item_gateaway import ItemGateaway
from project.services.electronics import validate_price, validate_weight, validate_ram_size, validate_cpu_cores, validate_hd_size, get_count
from re import match
from uuid import uuid4
import traceback


# Creates a tablet that is valid
def create_tablet(brand, price, weight, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info):
    try:
        if validate_price(price) and validate_weight(weight) and validate_ram_size(ram_size) and validate_cpu_cores(cpu_cores) and validate_hd_size(hd_size):

            tablet = Tablet(model=str(uuid4()), brand=brand, price=price, weight=weight,display_size=display_size, dimensions=dimensions, processor=processor,
                            ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, battery=battery, os=os, camera_info=camera_info)

            ItemGateaway.insert_into_db(tablet)
            TabletGateaway.insert_into_db(tablet)

            logger.info('Tablet created successfully!')

            return tablet

    except Exception as e:
        logger.error(traceback.format_exc())

# Queries the list of all tablets and their count
def get_all_tablets():
    try:
        rows = TabletGateaway.query_filtered_by()
        tablets = get_tablets_from_rows(rows)
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

# Returns all tablets from rows taken from db
def get_tablets_from_rows(rows):
    tablets=[]

    if rows:
        for row in rows:
            tablet = Tablet(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                            row[11], row[12])
            tablets.append(tablet)
        if tablets:
            return tablets
        else:
            return None
    else:
        return None
