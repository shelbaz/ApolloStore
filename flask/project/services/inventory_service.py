
from flask import g
from project import logger
from project.models import connect_to_db
from project.models.inventory_model import Inventory
from project.gateaways import delete_item
from project.gateaways.inventory_gateaway import InventoryGateaway
from re import match
from uuid import uuid4
import traceback


class InventoryService():


    # Adds an item of a specific model number to the inventory
    @staticmethod
    def add_item_to_inventory(model):
        try:
            inventory = Inventory(id=str(uuid4()), model=model)
            InventoryGateaway.insert_into_db(inventory)

            logger.info('Added %s to the inventory successfully!' % (model,))

            return inventory

        except Exception as e:
            logger.error(traceback.format_exc())

    # Returns all inventory items from rows taken from db
    @staticmethod
    def get_inventory_items_from_rows(rows):
        if rows:
            inventories = []

            for row in rows:
                inventory = Inventory(row[0], row[1])
                inventories.append(inventory)

            if inventories:
                return inventories
            else:
                return None
        else:
            return None
