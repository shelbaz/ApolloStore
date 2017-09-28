
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Tablet(Item):

    # Class function that creates the 'tablets' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'tablets'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('tablets',))

                # Creates table 'tablets' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE tablets (
                          model UUID PRIMARY KEY,
                          display_size varchar(64),
                          dimensions varchar(64),
                          processor varchar(64),
                          ram_size integer,
                          cpu_cores integer,
                          hd_size integer,
                          battery varchar(64),
                          os varchar(64),
                          camera_info varchar(64),
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Class function that deletes the 'tablets' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'tablets'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('tablets',))

                # Deletes table 'tablets' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE tablets;')

    # Constructor that creates a new tablet
    def __init__(self, model, brand, price, weight, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.display_size = display_size
        self.dimensions = dimensions
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.battery = battery
        self.os = os
        self.camera_info = camera_info

    # Adds the tablet to the database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                super().insert_into_db()
                cursor.execute(
                    """INSERT INTO tablets (model, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info) VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s');"""
                    % (self.model, self.display_size, self.dimensions, self.processor, str(self.ram_size), str(self.cpu_cores), str(self.hd_size), self.battery, self.os, self.camera_info))

    @staticmethod
    # Queries the tablets table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN tablets WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN tablets;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        tablets = []

        for row in rows:
            tablet = Tablet(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            tablets.append(tablet)

        if tablets:
            return tablets
        else:
            return None
