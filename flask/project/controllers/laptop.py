
from project import logger
from project.models.laptop import Laptop
from project.controllers.electronic import ElectronicController
from project.controllers.inventory import InventoryController
from uuid import uuid4
import traceback
from project.orm import Mapper
from project import identity_map

class LaptopController():

 

    # Creates a laptop that is valid
    @staticmethod
    def create_laptop(brand, price, weight, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera):
        try:
            if ElectronicController.validate_price(price) and ElectronicController.validate_weight(weight) and ElectronicController.validate_ram_size(ram_size) and ElectronicController.validate_cpu_cores(cpu_cores) and ElectronicController.validate_hd_size(hd_size):

                laptop = Laptop(model=str(uuid4()), brand=brand, price=price, weight=weight, display_size=display_size, processor=processor, ram_size=ram_size,
                                cpu_cores=cpu_cores, hd_size=hd_size, battery_info=battery_info, os=os, touchscreen=touchscreen, camera=camera)
                laptop.insert()
                identity_map.set(laptop.model, laptop)

                logger.info('Laptop created successfully!')

                return laptop

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def update_laptop(model, **conditions):
        inventory_rows = Mapper.query('inventories', model=model, locked=True)
        inventories = InventoryController.get_inventory_items_from_rows(inventory_rows)

        if not inventories:
            rows = Mapper.query('laptops', model=model)
            laptop = LaptopController.get_laptops_from_rows(rows)[0]
            laptop.update(**conditions)
            return laptop

    # Queries the list of all laptops and their count
    @staticmethod
    def get_all_laptops():
        try:
            rows = Mapper.query('items', 'laptops', hide=False)
            laptops = LaptopController.get_laptops_from_rows(rows)
            laptops_with_count = []

            if laptops:
                for laptop in laptops:
                    count = len(Mapper.query('inventories', 'laptops', model=laptop.model))
                    laptops_with_count.append([laptop.serialize(), count])

                return laptops_with_count
            else:
                return None
        except Exception:
            logger.error(traceback.format_exc())

        # Queries the list of all laptops and their count
    @staticmethod
    def get_all_unlocked_laptops(*filters):
        try:
            if filters == ():
                rows = Mapper.query('items', 'laptops', 'inventories', locked=False, hide=False)
            else:
                rows = Mapper.query('items', 'laptops', 'inventories', locked=False, hide=False, **filters[0])
                
            laptops = LaptopController.get_laptops_from_rows(rows)
            laptops_with_count = []

            if laptops:
                for laptop in laptops:
                    count = len(Mapper.query('inventories', 'laptops', model=laptop.model))
                    laptops_with_count.append([laptop.serialize(), count])
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
                if identity_map.getObject(row[0]):
                    laptop = identity_map.getObject(row[0])
                else:
                    
                    attributes = {}
                    index = 0

                    for key in Laptop.attributes.keys():
                        attributes[key] = row[index]
                        index += 1

                    laptop = Laptop(**attributes)

                    identity_map.set(laptop.model, laptop)
                    
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
            identity_map.delete(model)
            rows = Mapper.query('items', 'laptops', model=model)
            laptop = LaptopController.get_laptops_from_rows(rows)[0]

            laptop.update(model=model, brand = laptop.brand, price = laptop.price, weight = laptop.weight, display_size = laptop.display_size,
            processor = laptop.processor, ram_size = laptop.ram_size, cpu_cores = laptop.cpu_cores, hd_size = laptop.hd_size,
            battery_info = laptop.battery_info, os = laptop.os, touchscreen = laptop.touchscreen, camera = laptop.camera, hide=True)

            return laptop
        except Exception:
            logger.error(traceback.format_exc())