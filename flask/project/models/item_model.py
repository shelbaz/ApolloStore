
from project.models import connect_to_db
import psycopg2


class Item(object):

    # Class function that creates the 'items' table
    @staticmethod
    def create_table(*args):
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db(args) as connection:
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

    # Class function that deletes the 'items' table
    @staticmethod
    def drop_table(*args):
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db(args) as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'items'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('items',))

                # Creates table 'items' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE items;')


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
