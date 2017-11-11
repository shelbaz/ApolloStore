
from project import logger
from project.models.cart import Cart
from project.models.inventory import Inventory
from project.controllers.inventory import InventoryController
from project.identityMap import IdentityMap
from uuid import uuid4
import traceback
from time import gmtime, strftime
from project.orm import Mapper
from project import identity_map

class CartController():

    # Adds an item of a specific model number to the cart
    @staticmethod
    def add_item_to_cart(model, inventory_id, user_id):
        try:
            currentDateTime = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
            cart = Cart(id=str(uuid4()), model=model, inventory_id= inventory_id, user_id = user_id, added_time= currentDateTime)
            cart.insert()
            ## Lock item when added to cart
            InventoryController.update_inventory(model=model, inventory_id= inventory_id, locked=True)
            IdentityMap.set(cart.id, cart)
            logger.info('Added %s to the cart successfully!' % (model,))

            return cart

        except Exception:
            logger.error(traceback.format_exc())

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
                    InventoryController.update_inventory(model=model, inventory_id= inventory_id, locked=False)
                else:
                    logger.error("No more items in cart")
            else:
                logger.error("No items matching that query.")

        except Exception:
                logger.error(traceback.format_exc())

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




