
from project import logger
from project.models.cart import Cart
from project.models.inventory import Inventory
from project.controllers.inventory import InventoryController
from project.controllers.desktop import DesktopController
from project.controllers.tablet import TabletController
from project.controllers.laptop import LaptopController
from project.controllers.monitor import MonitorController
from project.identityMap import IdentityMap
from uuid import uuid4
import traceback
from time import gmtime, strftime
from project.orm import Mapper
from project import identity_map

class CartController():

    # Adds an item of a specific model number to the cart
    @staticmethod
    def add_item_to_cart(model, user_id):
        try:
            rows = Mapper.query('inventories', model=model)
            inventory_items = InventoryController.get_inventory_items_from_rows(rows)
            inventory_item=''
            for inv in inventory_items:
                if(not inv.locked):
                    inventory_item = inv

            currentDateTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            rows = CartController.count_number_items(user_id)

            if(inventory_item and rows < 7):
                cart = Cart(id=str(uuid4()), model=model, inventory_id= inventory_item.id, user_id = user_id, added_time= currentDateTime)
                cart.insert()
                # Lock item when added to cart
                InventoryController.update_inventory(model, inventory_item.id, locked=True, type=inventory_item.type)
                identity_map.set(cart.id, cart)
                logger.info('Added %s to the cart successfully!' % (model))

                return cart

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def count_number_items(user_id):
        rows = Mapper.count_rows(Cart, user_id)

        return rows

    # Removes an item of a specific model number from the cart
    @staticmethod
    def remove_item_from_cart(model, inventory_id, user_id):
        try:
            rows = Mapper.query('carts', user_id=user_id, inventory_id=inventory_id)
            if rows:
                cart_items = CartController.get_cart_items_from_rows(rows)
                cart = cart_items[0]
                identity_map.delete(cart.id)
                if cart:
                    cart.delete()
                    InventoryController.update_inventory(model=model, inventory_id=inventory_id, locked=False)
                else:
                    logger.error("No more items in cart")
            else:
                logger.error("No items matching that query.")

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def get_cart_items(user_id):
        rows = Mapper.query('carts', user_id=user_id)
        carts = CartController.get_cart_items_from_rows(rows)
        inventories = []
        returning=[]
        if carts:
            for cart in carts:
                rows = Mapper.query('inventories', model = cart.model)
                inventory = InventoryController.get_inventory_items_from_rows(rows)[0]
                inventories.append(inventory)

            for inventory in inventories:
                item=''
                if (inventory.type == 'desktops'):
                    rows = Mapper.query('items', 'desktops', model=inventory.model)
                    item = DesktopController.get_desktops_from_rows(rows)[0]
                elif (inventory.type == 'laptops'):
                    rows = Mapper.query('items', 'laptops', model=inventory.model)
                    item = LaptopController.get_laptops_from_rows(rows)[0]
                elif (inventory.type == 'tablets'):
                    rows = Mapper.query('items', 'tablets', model=inventory.model)
                    item = TabletController.get_tablets_from_rows(rows)[0]
                elif (inventory.type == 'monitors'):
                    rows = Mapper.query('items', 'monitors', model=inventory.model)
                    item = MonitorController.get_monitors_from_rows(rows)[0]

                returning.append(item)
            return returning


    # Returns all inventory items from rows taken from db
    @staticmethod
    def get_cart_items_from_rows(rows):
        if rows:
            carts = []
            for row in rows:
                if identity_map.getObject(row[0]):
                    cart = identity_map.getObject(row[0])
                else:
                    cart = Cart(row[0], row[1], row[2], row[3], row[4])
                    identity_map.set(cart.id, cart)

                carts.append(cart)

            if carts:
                return carts
            else:
                return None
        else:
            return None




