
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class TabletGateway(Item):

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

    # Adds the tablet to the database
    @staticmethod
    def insert_into_db(tablet):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO tablets (model, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info) VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s');"""
                    % (tablet.model, tablet.display_size, tablet.dimensions, tablet.processor, str(tablet.ram_size), str(tablet.cpu_cores), str(tablet.hd_size), tablet.battery, tablet.os, tablet.camera_info))

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

        if rows:
            return rows
        else:
            return None
