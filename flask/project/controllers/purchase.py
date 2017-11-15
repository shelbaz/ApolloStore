from project import logger
from project.models.purchase import Purchase
from project.controllers.inventory import InventoryController
from project.identityMap import IdentityMap
from flask import g
import datetime
import traceback
from project.orm import Mapper
from uuid import uuid4
from project import identity_map

class PurchaseController():

    @staticmethod
    def insert_into_table(model_id):
        try:
            added_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            purchase = Purchase(id=str(uuid4()), user_id=g.user.id, added_time=added_time, model_id=model_id)
            purchase.insert()
            logger.info('Purchase created successfully!')

        except Exception:
            logger.error(traceback.format_exc())

            # Returns all monitors from rows taken from db

    @staticmethod
    def get_purchases_from_rows(rows):
        if rows:
            purchases = []
            for row in rows:
                purchase = Purchase(row[0], row[1], row[2], row[3])
                purchases.append(purchase)

            if purchases:
                return purchases
            else:
                return None
        else:
            return None

    # deletes item from purchase table
    @staticmethod
    def delete_purchases(model_id):
        try:
            rows = Mapper.query('purchases', model_id=model_id, user_id=g.user.id)
            if rows:
                purchase_items = PurchaseController.get_purchases_from_rows(rows)
                purchase = purchase_items[0]
                identity_map.delete(purchase.id)
                if purchase:
                    purchase.delete()
                else:
                    logger.error("No more purchases")
            else:
                logger.error("No purchase made by user")
        except Exception:
            logger.error(traceback.format_exc())


    @staticmethod
    def get_past_purchases():
        rows = Mapper.query('purchases', user_id=g.user.id)
        purchases = PurchaseController.get_purchases_from_rows(rows)
        purchase_items = []
        for purchase in purchases:
            purchase_items.append(purchase)
        return purchase_items


    @staticmethod
    def return_past_purchase(model):
         rows = Mapper.query('purchases', user_id=g.user.id, model_id=model)
         purchases = PurchaseController.get_purchases_from_rows(rows)
         if purchases:
            InventoryController.add_item_to_inventory(model, purchases.type)
            PurchaseController.delete_purchases(model)



