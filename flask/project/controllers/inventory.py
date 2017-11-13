
from project import logger
from project.models.inventory import Inventory
from project.gateways import get_inventory_count
from project.identityMap import IdentityMap
from uuid import uuid4
import traceback
from project.orm import Mapper
from project import identity_map

class InventoryController():

    identityMap = IdentityMap()

    # Adds an item of a specific model number to the inventory
    @staticmethod
    def add_item_to_inventory(model, type):
        try:
            inventory = Inventory(id=str(uuid4()), model=model, type=type) 
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
                if identity_map.getObject(row[0]):
                    inventory = identity_map.getObject(row[0])
                else:
                    inventory = Inventory(row[0], row[1], row[2])
                    identity_map.set(inventory.id, inventory)

                inventories.append(inventory)

            if inventories:
                return inventories
            else:
                return None
        else:
            return None


    # Returns all inventory items not locked for item type
    @staticmethod
    def get_inventory_not_locked(type):
        try:
            rows = Mapper.query('inventories', type=type.lower(), locked=False)
            inventory = InventoryController.get_inventory_items_from_rows(rows)
            inventory_with_count = []

            if inventory:
                for item in inventory:
                    itemType = None
                    if type == 'Desktop':
                        itemType = 'desktops'
                    elif type == 'Laptop':
                        itemType = 'laptops'
                    elif type == 'Tablet':
                        itemType = 'tablets'
                    elif type == 'Monitor':
                        itemType = 'monitors'
                    count = get_inventory_count(itemType, item.model)
                    inventory_with_count.append([inventory, count])
                return inventory_with_count
            else:
                return None
        except Exception:
            logger.error(traceback.format_exc())



    # Deletes an item from the inventory after checkout
    @staticmethod
    def delete_item_from_inventory(model, inventoryid):
        rows = Mapper.query('inventories', model=model, inventoryid=inventoryid)
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

    # Updates inventory item with matching model with a condition
    @staticmethod
    def update_inventory(model, inventoryid, **conditions):
        rows = Mapper.query('inventories', model=model, id=inventoryid)
        inventoryItem = InventoryController.get_inventory_items_from_rows(rows)[0]
        inventoryItem.update(**conditions)
        return inventoryItem

        
        