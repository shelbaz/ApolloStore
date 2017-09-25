
from project.models import connect_to_db
import psycopg2


class Item(object):

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
                          price decimal,
                          weight decimal,
                          brand varchar(64)
                        );
                        """
                    )

    # Constructor that creates a new item
    def __init__(self, model, price, weight, brand):

        # Initializes object attributes
        self.model = model
        self.price = price
        self.weight = weight
        self.brand = brand

    # Adds the item to the database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO items (model, price, weight, brand) VALUES ('%s', %s, %s, '%s');"""
                    % (self.model, str(self.price), str(self.weight), self.brand))


    # Queries the items table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        query = """SELECT * FROM items WHERE %s;""" % (filters,)

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        items = []

        for row in rows:
            items = Item(row[0], row[1], row[2], row[3])
            items.append(items)

        if items:
            return items
        else:
            return None