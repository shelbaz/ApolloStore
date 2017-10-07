
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class LaptopGateaway(Item):

    # Class function that creates the 'laptops' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'laptops'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('laptops',))

                # Creates table 'laptops' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE laptops (
                          model UUID PRIMARY KEY,
                          display_size varchar(64),
                          processor varchar(64),
                          ram_size integer,
                          cpu_cores integer,
                          hd_size integer,
                          battery_info varchar(64),
                          os varchar(64),
                          touchscreen boolean,
                          camera boolean,
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Class function that deletes the 'laptops' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'laptops'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('laptops',))

                # Deletes table 'laptops' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE laptops;')

    # Adds the laptop to the database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                super().insert_into_db()
                cursor.execute(
                    """INSERT INTO laptops (model, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera) VALUES ('%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s', '%s');"""
                    % (self.model, self.display_size, self.processor, str(self.ram_size), str(self.cpu_cores), str(self.hd_size), self.battery_info, self.os, str(self.touchscreen), str(self.camera)))


    @staticmethod
    # Queries the laptops table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN laptops WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN laptops;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

        '''
        laptops = []

        for row in rows:
            laptop = Laptop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            laptops.append(laptop)

        if laptops:
            return laptops
        else:
            return None
        '''