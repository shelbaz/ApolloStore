
from project import logger
from project.models.cart import Cart
from project.models.inventory import Inventory
from project.controllers.electronic import ElectronicController
from project.controllers.inventory import InventoryController
from project.controllers.purchase import PurchaseController
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
    def remove_item_from_cart(model, user_id):
        try:
            rows = Mapper.query('carts', model=model, user_id=user_id)
            if rows:
                cart_items = CartController.get_cart_items_from_rows(rows)
                cart = cart_items[0]
                identity_map.delete(cart.id)
                logger.error('something')
                if cart:
                    inv_id = cart.inventory_id
                    cart.delete(cart.id)
                    InventoryController.update_inventory(model=model, inventory_id=inv_id, locked=False)
                else:
                    logger.error('No more items in cart')
            else:
                logger.error('No items matching that query.')

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def get_cart_items(user_id):
        rows = Mapper.query('carts', user_id=user_id)
        carts = CartController.get_cart_items_from_rows(rows)
        cart_items = []
        if carts:
            for cart in carts:
                rows = Mapper.query('items', model = cart.model)
                inventory = ElectronicController.get_items_from_rows(rows)[0]
                cart_items.append(inventory)

            return cart_items

    #Takes items from cart and adds them to purchases db log, removes items from inventory and flushes cart
    @staticmethod
    def checkout_from_cart(user_id):
        rows = Mapper.query('carts', user_id=user_id)
        carts = CartController.get_cart_items_from_rows(rows)
        if carts:
            for cart in carts:
                PurchaseController.insert_into_table(user_id=user_id, model=cart.model)
                InventoryController.delete_item_from_inventory(model=cart.model, inventoryid=cart.inventory_id)
                identity_map.delete(cart.id)
                logger.info('Deleted %s from the inventory successfully!' % (cart.model))
        CartController.flush_cart()
        logger.info('Cart flushed successfully!')

    #Removes all items from cart with selected user_id
    @staticmethod
    def flush_cart(user_id):
        rows = Mapper.query('carts', user_id=user_id)
        carts = CartController.get_cart_items_from_rows(rows)
        if carts:
            for cart in carts:
                Mapper.delete(cart.id)
                logger.info('Deleted %s from the cart successfully!' % (cart.model))

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



