
from project.models import connect_to_db
import psycopg2


class ItemGateaway(object):

    # Class function that creates the 'items' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'items'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('items',))

                # Creates table 'items' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE items (
                          model UUID PRIMARY KEY,
                          brand varchar(64),
                          price decimal,
                          weight decimal
                        );
                        """
                    )

    # Class function that deletes the 'items' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'items'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('items',))

                # Creates table 'items' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE items;')

    # Adds the item to the database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO items (model, brand, price, weight) VALUES ('%s', '%s', %s, %s);"""
                    % (self.model, self.brand, str(self.price), str(self.weight)))

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