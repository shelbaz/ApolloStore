
from project.models import connect_to_db


class ItemGateway(object):

    # Adds the item to the database
    @staticmethod
    def insert_into_db(item):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO items (model, brand, price, weight) VALUES ('%s', '%s', %s, %s);"""
                    % (item.model, item.brand, str(item.price), str(item.weight)))
