from project.models import connect_to_db
import psycopg2


class CartGateway(object):

    # Insert cart into database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO carts (id, inventory_id, user_id, added_time) VALUES ('%s', '%s', '%s', '%s');"""
                    % (self.id, self.inventory_id, self.user_id, self.added_time))

    @staticmethod
    # Queries the carts table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM carts WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM carts;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

        '''
        carts = []

        for row in rows:
            carts = Cart(row[0], row[1], row[2], row[3])
            carts.append(carts)

        if carts:
            return carts
        else:
            return None
        '''