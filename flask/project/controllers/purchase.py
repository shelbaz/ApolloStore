from project import logger
from project.models.purchase import Purchase
from project.controllers.inventory import InventoryController
from flask import g
import datetime
import traceback
from project.orm import Mapper
from uuid import uuid4
from project import identity_map
from project.contract import Contract

class PurchaseController():

    @staticmethod
    @Contract.purchase_item
    def insert_into_table(model_id):
        try:
            rows = Mapper.query('inventories', model=model_id)
            if rows:
                inventoryItem = InventoryController.get_inventory_items_from_rows(rows)[0]
                added_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                purchase = Purchase(id=str(uuid4()), user_id=g.user.id, added_time=added_time, model_id=model_id, type=inventoryItem.type)
                purchase.insert()
                logger.info('Purchase created successfully!')

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def get_purchases_from_rows(rows):
        if rows:
            purchases = []
            for row in rows:
                purchase = Purchase(row[0], row[1], row[2], row[3], row[4])
                purchases.append(purchase)

            if purchases:
                return purchases
            else:
                return []
        else:
            return []

    # deletes item from purchase table
    @staticmethod
    def delete_purchases(model_id):
        try:
            rows = Mapper.query('purchases', model_id=model_id, user_id=g.user.id)
            if rows:
                purchase = PurchaseController.get_purchases_from_rows(rows)[0]
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
        if rows:
            purchases = PurchaseController.get_purchases_from_rows(rows)
            purchase_items = []
            for purchase in purchases:
                purchase_items.append(purchase)
            return purchase_items


    @staticmethod
    @Contract.return_item_to_store
    def return_item(model):
        rows = Mapper.query('purchases', model_id=model)
        if rows:
             purchaseItem = PurchaseController.get_purchases_from_rows(rows)[0]
             InventoryController.add_item_to_inventory(model, purchaseItem.type)
             PurchaseController.delete_purchases(model)



