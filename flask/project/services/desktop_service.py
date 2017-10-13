
from flask import g
from project import logger
from project.models import connect_to_db
from project.gateaways import delete_item
from project.models.desktop_model import Desktop
from project.gateaways.desktop_gateaway import DesktopGateaway
from project.gateaways.item_gateaway import ItemGateaway
from project.models.item_model import Item
from project.services.electronic_service import ElectronicService
from project.services.inventory_service import InventoryService
from project.gateaways.inventory_gateaway import InventoryGateaway
from project.identityMap import IdentityMap
# from project.services.abstract_service import AbstractService
from re import match
from uuid import uuid4
import traceback

class DesktopService():

    identityMap = IdentityMap()

    # Creates a desktop that is valid
    @staticmethod
    def create_desktop(brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):
        try:
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight) and ElectronicService.validate_ram_size(ram_size) and ElectronicService.validate_cpu_cores(cpu_cores) and ElectronicService.validate_hd_size(hd_size):
                desktop = Desktop(model=str(uuid4()), brand=brand, price=price, weight=weight, processor=processor,
                                  ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, dimensions=dimensions)

                DesktopService.identityMap.set(desktop.model, desktop)

                return desktop

        except Exception as e:
            logger.error(traceback.format_exc())

    @staticmethod
    def insert_desktop(desktop):
        ItemGateaway.insert_into_db(desktop)
        DesktopGateaway.insert_into_db(desktop)
        logger.info('Desktop created successfully!')

    @staticmethod
    def update_desktop(model, brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):
        try:
            rows = DesktopGateaway.query_filtered_by(model=model)
            desktop1 = DesktopService.get_desktops_from_rows(rows)[0]
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight) and ElectronicService.validate_ram_size(ram_size) and ElectronicService.validate_cpu_cores(cpu_cores) and ElectronicService.validate_hd_size(hd_size):
                desktop2 = Desktop(model=model, brand=brand, price=price, weight=weight, processor=processor,
                                  ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, dimensions=dimensions)
                DesktopGateaway.remove_from_db(desktop1)
                ItemGateaway.remove_from_db(desktop1)
                ItemGateaway.insert_into_db(desktop2)
                DesktopGateaway.insert_into_db(desktop2)
                DesktopService.identityMap.set(desktop2.model, desktop2)

                logger.info('Desktop updated successfully!')

                return desktop2

        except Exception as e:
            logger.error(traceback.format_exc())

    # Queries the list of all desktops and their count
    @staticmethod
    def get_all_desktops():
        try:
            rows = DesktopGateaway.query_filtered_by()
            desktops = DesktopService.get_desktops_from_rows(rows)
            desktops_with_count = []

            if desktops:
                for desktop in desktops:
                    count = InventoryGateaway.get_count('desktops', desktop.model)
                    desktops_with_count.append([desktop, count])
                return desktops_with_count
            else:
                return None
        except Exception as e:
            logger.error(traceback.format_exc())

    # Returns all desktops from rows taken from db
    @staticmethod
    def get_desktops_from_rows(rows):
        if rows:
            desktops = []
            for row in rows:
                #check identity map
                if DesktopService.identityMap.hasId(row[0]):
                    logger.debug("found object in identity map")
                    desktop = DesktopService.identityMap.getObject(row[0])
                else:
                    logger.debug("inserting desktop into identity map")
                    desktop = Desktop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    DesktopService.identityMap.set(desktop.model, desktop)

                desktops.append(desktop)

            if desktops:
                return desktops
            else:
                return None
        else:
            return None

