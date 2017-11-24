
from project import logger, create_app
from project.models.cart import Cart
from flask import g
from project.controllers.inventory import InventoryController
from project.controllers.purchase import PurchaseController
from uuid import uuid4
import traceback
from project.orm import Mapper
from project import identity_map
from datetime import datetime, timedelta
from project import celery
import time

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

            logger.info(inventory_item.type)

            item_timeout = datetime.now()
            if inventory_item.type == 'Desktop':
                item_timeout = time.mktime((datetime.now() + timedelta(seconds=45)).timetuple())
            elif inventory_item.type == 'Laptop':
                item_timeout = time.mktime((datetime.now() + timedelta(seconds=65)).timetuple())
            elif inventory_item.type == 'Tablet':
                item_timeout = time.mktime((datetime.now() + timedelta(seconds=85)).timetuple())
            elif inventory_item.type == 'Monitor':
                item_timeout = time.mktime((datetime.now() + timedelta(seconds=95)).timetuple())

            rows = CartController.get_number_of_items_in_cart()

            if(inventory_item and rows < 7):
                cart = Cart(id=str(uuid4()), model=model, inventory_id=inventory_item.id, user_id=g.user.id, expiry_time=item_timeout)
                cart.insert()
                # Lock item when added to cart
                InventoryController.update_inventory(model, inventory_item.id, locked=True, type=inventory_item.type)
                identity_map.set(cart.id, cart)
                logger.info('Added %s to the cart successfully!' % (model))

                CartController.cart_timeout()

                return cart

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def get_number_of_items_in_cart():
        items = CartController.get_cart_items()
        return len(items)

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
        
        items = []

        if carts:
            cart_models = {}

            for cart in carts:
                if cart.model in cart_models.keys():
                    cart_models[cart.model] += 1
                else:
                    cart_models[cart.model] = 1

            rows = Mapper.all_items_query(cart_models.keys())
            items = CartController.get_items_from_rows(rows)

        cart_items = []

        for item in items:
             cart_items.extend([item] * cart_models[item['model']])

        return cart_items

    @staticmethod
    def get_items_from_rows(rows):
        items = []
        for row in rows:
            items.append({'model': row[0], 'brand': row[1], 'price': row[2]})
        return items

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
                return []
        else:
            return []

    @staticmethod
    @celery.task(name='cart_timeout')
    def cart_timeout():
        with create_app().app_context():
            rows = Mapper.query('carts')
            carts = CartController.get_cart_items_from_rows(rows)
            for item in carts:
                current_time = datetime.now()
                expiry = datetime.fromtimestamp(item.expiry_time)
                if expiry < current_time:
                    try:

                        identity_map.delete(item.id)
                        item.delete()
                        logger.info('cart inventory id:' + item.inventory_id)
                        InventoryController.update_inventory(item.model, inventoryid=item.inventory_id, locked=False)
                        logger.info('Added %s back to inventory successfully!' % (item.model))

                    except Exception:
                        logger.error(traceback.format_exc())
