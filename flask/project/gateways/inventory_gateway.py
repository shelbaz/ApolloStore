
from project.models import connect_to_db
import psycopg2
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

    @staticmethod
    # Queries the inventory table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM inventories WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM inventories;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

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
        except Exception as e:
            logger.error(traceback.format_exc())

