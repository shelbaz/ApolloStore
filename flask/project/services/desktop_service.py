
from project import logger
from project.gateways import get_inventory_count
from project.models.desktop_model import Desktop
from project.services.electronic_service import ElectronicService
from project.identityMap import IdentityMap
from uuid import uuid4
import traceback
from project.orm import Mapper


class DesktopService():

    identityMap = IdentityMap()

    # Creates a desktop that is valid
    @staticmethod
    def create_desktop(brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):
        try:
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight) and ElectronicService.validate_ram_size(ram_size) and ElectronicService.validate_cpu_cores(cpu_cores) and ElectronicService.validate_hd_size(hd_size):
                desktop = Desktop(model=str(uuid4()), brand=brand, price=price, weight=weight, processor=processor,
                                  ram_size=ram_size, cpu_cores=cpu_cores, hd_size=hd_size, dimensions=dimensions)
                desktop.insert()
                DesktopService.identityMap.set(desktop.model, desktop)

                logger.info('Desktop created successfully!')

                return desktop

        except Exception:
            logger.error(traceback.format_exc())

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
            rows = Mapper.query('items', 'desktops')
            desktops = DesktopService.get_desktops_from_rows(rows)
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

    @staticmethod
    def delete_model(model):
        try:
            rows = Mapper.query('items', 'desktops', model=model)
            desktop = DesktopService.get_desktops_from_rows(rows)[0]

            desktop.delete()

        except Exception:
            logger.error(traceback.format_exc())
