from project import logger
from project.models.purchase import Purchase
import datetime
import traceback
from project.orm import Mapper
from uuid import uuid4

class PurchaseController():

    @staticmethod
    def insert_into_table(user_id, model_id):
        try:
            added_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            purchase = Purchase(id=str(uuid4()), user_id=user_id, added_time=added_time, model_id=model_id)
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

    @staticmethod
    def delete_purchases(user_id, model_id):
        try:
            rows = Mapper.query('purchases', model_id=model_id, user_id=user_id)
            purchase = PurchaseController.get_monitors_from_rows(rows)[0]

            purchase.delete()

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def get_past_purchases(user_id):
        rows = Mapper.query('purchases', user_id=user_id)
        purchases = PurchaseController.get_purchases_from_rows(rows)
        purchase_items = []
        if purchases:
            for purchase in purchases:
                purchase_items.append(purchase.model_id)
            return purchase_items