
from project import logger
from project.models.cart import Cart
from flask import g
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
    def add_item_to_cart(model):
        try:
            rows = Mapper.query('inventories', model=model)
            inventory_items = InventoryController.get_inventory_items_from_rows(rows)
            inventory_item=''
            for inv in inventory_items:
                if(not inv.locked):
                    inventory_item = inv

            currentDateTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            rows = CartController.count_number_items()

            if(inventory_item and rows < 7):
                cart = Cart(id=str(uuid4()), model=model, inventory_id=inventory_item.id, user_id=g.user.id, added_time=currentDateTime)
                cart.insert()
                # Lock item when added to cart
                InventoryController.update_inventory(model, inventory_item.id, locked=True, type=inventory_item.type)
                identity_map.set(cart.id, cart)
                logger.info('Added %s to the cart successfully!' % (model))

                return cart

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def count_number_items():
        rows = Mapper.count_rows(Cart, g.user.id)

        return rows

    # Removes an item of a specific model number from the cart
    @staticmethod
    def remove_item_from_cart(model):
        logger.critical('something')
        try:

            rows = Mapper.query('carts', model=model, user_id=g.user.id)
            if rows:
                cart_items = CartController.get_cart_items_from_rows(rows)
                cart = cart_items[0]
                if cart:
                    identity_map.delete(cart.id)
                    inv_id = cart.inventory_id
                    cart.delete()
                    logger.info('cart inventory id:' + inv_id)
                    InventoryController.update_inventory(model=model, inventoryid=inv_id, locked=False)
                    logger.info('Added %s back to inventory successfully!' % (model))

                else:
                    logger.error('No more items in cart')
            else:
                logger.error('No items matching that query.')

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def get_cart_items():
        rows = Mapper.query('carts', user_id=g.user.id)
        carts = CartController.get_cart_items_from_rows(rows)
        
        if carts:
            cart_models = []

            for cart in carts:
                cart_models.append(cart.model)

            rows = Mapper.all_items_query(cart_models)
            items = CartController.get_items_from_rows(rows)
        
            return items

    @staticmethod
    def get_items_from_rows(rows):
        if rows:
            items = []
            for row in rows:
                items.append({'model': row[0], 'brand': row[1], 'price': row[2]})

            if items:
                return items
            else:
                return None

    #Takes items from cart and adds them to purchases db log, removes items from inventory and flushes cart
    @staticmethod
    def checkout_from_cart():
        rows = Mapper.query('carts', user_id=g.user.id)
        carts = CartController.get_cart_items_from_rows(rows)
        if carts:
            for cart in carts:
                PurchaseController.insert_into_table(model_id=cart.model)
                my_model = cart.model
                inv_id = cart.inventory_id
                identity_map.delete(cart.id)
                cart.delete()
                InventoryController.delete_item_from_inventory(my_model, inv_id)

                logger.info('Deleted %s from the inventory successfully!' % (cart.model))

        logger.info('Cart flushed successfully!')

    #Removes all items from cart with selected user_id (to be used with timer)
    @staticmethod
    def flush_cart():
        rows = Mapper.query('carts', user_id=g.user.id)
        carts = CartController.get_cart_items_from_rows(rows)
        if carts:
            for cart in carts:
                InventoryController.update_inventory(model=cart.model, inventoryid=cart.inventory_id, locked=False)
                logger.info('Added %s back to inventory successfully!' % (cart.model))
                cart.delete()
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




