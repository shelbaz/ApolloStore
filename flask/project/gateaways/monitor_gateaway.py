
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2

class MonitorGateaway(Item):

    # Class function that creates the 'monitors' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'monitors'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('monitors',))

                # Creates table 'monitors' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE monitors (
                          model UUID PRIMARY KEY,
                          dimensions varchar(64),
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Class function that deletes the 'monitors' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'monitors'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('monitors',))

                # Deletes table 'monitors' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE monitors;')

    # Adds the monitor to the database
    @staticmethod
    def insert_into_db(monitor):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO monitors (model, dimensions) VALUES ('%s', '%s');"""
                    % (monitor.model, monitor.dimensions))

    # Removes the monitor to the database
    @staticmethod
    def remove_from_db(monitor):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM monitors WHERE model='%s';"""
                    % monitor.model)

    @staticmethod
    # Queries the monitors table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN monitors WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN monitors;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

