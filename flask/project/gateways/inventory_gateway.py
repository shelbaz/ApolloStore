
from project.models import connect_to_db
from project import logger
import traceback

class InventoryGateway(object):

    # Insert inventory into database
    @staticmethod
    def insert_into_db(inventory):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO inventories (id, model) VALUES ('%s', '%s');"""
                    % (inventory.id, inventory.model))

    # Gets count of items in inventory for a model
    @staticmethod
    def get_count(electronic_type, model):
        try:
            query = 'SELECT COUNT(*) FROM inventories NATURAL JOIN (SELECT * FROM %s WHERE model=\'%s\') AS x;' % (electronic_type, model)
            with connect_to_db() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    count = cursor.fetchone()
            return count[0]
        except Exception:
            logger.error(traceback.format_exc())
