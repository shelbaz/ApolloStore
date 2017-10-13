
from project import logger
from project.models.laptop_model import Laptop
from project.gateways import get_inventory_count
from project.identityMap import IdentityMap
from project.services.electronic_service import ElectronicService
from uuid import uuid4
import traceback


class LaptopService():

    identityMap = IdentityMap()

    # Creates a laptop that is valid
    @staticmethod
    def create_laptop(brand, price, weight, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera):
        try:
            if ElectronicService.validate_price(price) and ElectronicService.validate_weight(weight) and ElectronicService.validate_ram_size(ram_size) and ElectronicService.validate_cpu_cores(cpu_cores) and ElectronicService.validate_hd_size(hd_size):

                laptop = Laptop(model=str(uuid4()), brand=brand, price=price, weight=weight, display_size=display_size, processor=processor, ram_size=ram_size,
                                cpu_cores=cpu_cores, hd_size=hd_size, battery_info=battery_info, os=os, touchscreen=touchscreen, camera=camera)
                laptop.insert()
                LaptopService.identityMap.set(laptop.model, laptop)

                logger.info('Laptop created successfully!')

                return laptop

        except Exception:
            logger.error(traceback.format_exc())

    # Queries the list of all laptops and their count
    @staticmethod
    def get_all_laptops():
        try:
            rows = Laptop.query()
            laptops = LaptopService.get_laptops_from_rows(rows)
            laptops_with_count = []

            if laptops:
                for laptop in laptops:
                    count = get_inventory_count('laptops', laptop.model)
                    laptops_with_count.append([laptop, count])
                return laptops_with_count
            else:
                return None
        except Exception:
            logger.error(traceback.format_exc())

    # Returns all laptops from rows taken from db
    @staticmethod
    def get_laptops_from_rows(rows):
        laptops = []

        if rows:
            for row in rows:
                #check identity map
                if LaptopService.identityMap.hasId(row[0]):
                    laptop = LaptopService.identityMap.getObject(row[0])
                else:
                    laptop = Laptop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                row[11], row[12])
                    LaptopService.identityMap.set(laptop.model, laptop)
                    
                laptops.append(laptop)

            if laptops:
                return laptops
            else:
                return None
        else:
            return None

    @staticmethod
    def delete_model(model):
        try:
            rows = Laptop.query(model=model)
            laptop = LaptopService.get_laptops_from_rows(rows)[0]

            laptop.delete()

        except Exception:
            logger.error(traceback.format_exc())
