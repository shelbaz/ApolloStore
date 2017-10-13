
from project.models import connect_to_db
import psycopg2


class ItemGateaway(object):

    # Adds the item to the database
    @staticmethod
    def insert_into_db(item):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO items (model, brand, price, weight) VALUES ('%s', '%s', %s, %s);"""
                    % (item.model, item.brand, str(item.price), str(item.weight)))

    @staticmethod
    # Queries the items table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

        '''
        items = []

        for row in rows:
            item = Item(row[0], row[1], row[2], row[3])
            items.append(items)

        if items:
            return items
        else:
            return None
        '''