
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

    identityMap = IdentityMap()

    # Adds an item of a specific model number to the cart
    @staticmethod
    def add_item_to_cart(model, inventory_id, user_id):
        try:
            currentDateTime = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
            cart = Cart(id=str(uuid4()), model=model, inventory_id= inventory_id, user_id = user_id, added_time= currentDateTime)
            cart.insert()
            ## Lock item when added to cart
            InventoryController.update_inventory(model=model, inventory_id= inventory_id, locked=True)
            identity_map.set(cart.id, cart)
            logger.info('Added %s to the cart successfully!' % (model,))

            return cart

        except Exception:
            logger.error(traceback.format_exc())

    # @staticmethod
    # def remove_item_from_cart(inventory_id)


