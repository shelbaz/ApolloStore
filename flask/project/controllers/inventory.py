
from project import logger
from project.models.inventory import Inventory
from project.identityMap import IdentityMap
from uuid import uuid4
import traceback
from project.orm import Mapper
from project import identity_map

class InventoryController():

    identityMap = IdentityMap()

    # Adds an item of a specific model number to the inventory
    @staticmethod
    def add_item_to_inventory(model):
        try:
            inventory = Inventory(id=str(uuid4()), model=model)
            inventory.insert()
            identity_map.set(inventory.id, inventory)
            logger.info('Added %s to the inventory successfully!' % (model,))

            return inventory

        except Exception:
            logger.error(traceback.format_exc())

    # Returns all inventory items from rows taken from db
    @staticmethod
    def get_inventory_items_from_rows(rows):
        if rows:
            inventories = []

            for row in rows:
                #check identity map
                if identity_map.getObject(row[0]):
                    inventory = identity_map.getObject(row[0])
                else:
                    inventory = Inventory(row[0], row[1])
                    identity_map.set(inventory.id, inventory)

                inventories.append(inventory)

            if inventories:
                return inventories
            else:
                return None
        else:
            return None

    @staticmethod
    def delete_item_from_inventory(model):
        rows = Mapper.query('inventories', model=model)
        if rows:
            inventory_items = InventoryController.get_inventory_items_from_rows(rows)
            inventory = inventory_items[0]
            identity_map.delete(inventory.id)
            if inventory:
                inventory.delete()
            else:
                logger.error("No more of type item in inventory")
        else:
            logger.error("No items.")
        