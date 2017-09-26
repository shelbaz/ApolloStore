
from project.models import connect_to_db
import psycopg2


class Inventory(object):

    # Class function that creates the 'inventories' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'inventories'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('inventories',))

                # Creates table 'inventories' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE inventories (
                          id UUID PRIMARY KEY,
                          model UUID,
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Class function that deletes the 'inventories' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'inventories'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('inventories',))

                # Creates table 'users' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE inventories;')

    # Constructor that creates inventory
    def __init__(self, id, model):

        # Initialize object attributes
        self.id = id
        self.model = model

    # Insert inventory into database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO inventories (id, model) VALUES ('%s', '%s');"""
                    % (self.id, self.model))

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

        inventory = []

        for row in rows:
            inventory = Inventory(row[0], row[1])
            inventory.append(inventory)

        if inventory:
            return inventory
        else:
            return None