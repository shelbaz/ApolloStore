
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2

class DesktopGateway(Item):

    # Class function that creates the 'desktops' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'desktops'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('desktops',))

                # Creates table 'desktops' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE desktops (
                          model UUID PRIMARY KEY,
                          processor varchar(64),
                          ram_size integer,
                          cpu_cores integer,
                          hd_size integer,
                          dimensions varchar(64),
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Class function that deletes the 'desktops' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'desktops'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('desktops',))

                # Deletes table 'desktops' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE desktops;')

    # Adds the desktop to the database
    @staticmethod
    def insert_into_db(desktop):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO desktops (model, processor, ram_size, cpu_cores, hd_size, dimensions) VALUES ('%s', '%s', %s, %s, %s, '%s');"""
                    % (desktop.model, desktop.processor, str(desktop.ram_size), str(desktop.cpu_cores), str(desktop.hd_size), desktop.dimensions))

    @staticmethod
    # Queries the desktops table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN desktops WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN desktops;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
