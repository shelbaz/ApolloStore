
from project import logger
from project.gateways import get_inventory_count
from project.models.desktop import Desktop
from project.controllers.electronic import ElectronicController
from uuid import uuid4
import traceback
from project.orm import Mapper
from project import identity_map

class DesktopController():



    # Creates a desktop that is valid
    @staticmethod
    def create_desktop(brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):
        try:
            if ElectronicController.validate_price(price) and ElectronicController.validate_weight(weight) and ElectronicController.validate_ram_size(ram_size) and ElectronicController.validate_cpu_cores(cpu_cores) and ElectronicController.validate_hd_size(hd_size):
                desktop = Desktop(model=str(uuid4()), brand=brand, price=price, weight=weight, processor=processor,
                                  ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, dimensions=dimensions)
                desktop.insert()
                identity_map.set(desktop.model, desktop)

                logger.info('Desktop created successfully!')

                return desktop

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def update_desktop(model, **conditions):
        rows = Mapper.query('desktops', model=model)
        desktop = DesktopController.get_desktops_from_rows(rows)[0]
        desktop.update(**conditions)
        return desktop

    # Queries the list of all desktops and their count
    @staticmethod
    def get_all_desktops():
        try:
            rows = Mapper.query('items', 'desktops')
            desktops = DesktopController.get_desktops_from_rows(rows)
            desktops_with_count = []

            if desktops:
                for desktop in desktops:
                    count = get_inventory_count('desktops', desktop.model)
                    desktops_with_count.append([desktop, count])
                return desktops_with_count
            else:
                return None
        except Exception:
            logger.error(traceback.format_exc())

    # Returns all desktops from rows taken from db
    @staticmethod
    def get_desktops_from_rows(rows):
        if rows:
            desktops = []
            for row in rows:
                #check identity map
                if identity_map.getObject(row[0]):
                    logger.debug("found object in identity map")
                    desktop = identity_map.getObject(row[0])
                else: 
                    logger.debug("inserting desktop into identity map")
                    desktop = Desktop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    identity_map.set(desktop.model, desktop)

                desktops.append(desktop)

            if desktops:
                return desktops
            else:
                return None
        else:
            return None

    @staticmethod
    def delete_model(model):
        try:
            identity_map.delete(model)
            rows = Mapper.query('items', 'desktops', model=model)
            desktop = DesktopController.get_desktops_from_rows(rows)[0]

            desktop.delete()

        except Exception:
            logger.error(traceback.format_exc())