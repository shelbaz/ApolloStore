
import psycopg2
import time
import os
from flask import current_app


# Creates a connection to the PostgreSQL using the test database if an argument is passed, and using the dev database if none is passed
def connect_to_db():
    if current_app.config['TESTING']:
        with psycopg2.connect(os.getenv('DATABASE_TEST_URL')) as connection:
            return connection
    else:
        with psycopg2.connect(os.getenv('DATABASE_URL')) as connection:
            return connection


def create_table(name, attributes, constraints, *enum):
    # Using the 'with' statement automatically commits and closes database connections
    with connect_to_db() as connection:
        with connection.cursor() as cursor:

            # Searches if there is already a table with the same name
            cursor.execute("select * from information_schema.tables where table_name=%s", (name,))

            query = ''

            # Adds ENUM type if existent
            if enum:
                for key, value in enum[0].items():
                    query += """
                            DO $$
                            BEGIN
                                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'types') THEN
                                    CREATE TYPE %s AS ENUM %s;
                                END IF;
                            END$$;
                            """ % (key, value)

            query += 'CREATE TABLE %s (' % name

            # Adds attributes
            for key, value in attributes.items():
                query += '%s %s, ' % (key, value)

            currently_first_constraint = True

            # Adds constraints
            for key, value in constraints.items():
                if currently_first_constraint:
                    query += '%s %s' % (key, value)
                    currently_first_constraint = False
                else:
                    query += ', %s %s' % (key, value)

            query += ');'

            if not bool(cursor.rowcount):
                cursor.execute(query)


def drop_table(name):
    # Using the 'with' statement automatically commits and closes database connections
    with connect_to_db() as connection:
        with connection.cursor() as cursor:
            # Searches if there is already a table with the same name
            cursor.execute("select * from information_schema.tables where table_name=%s", (name,))

            # Deletes table if it exists
            if bool(cursor.rowcount):
                cursor.execute('DROP TABLE %s;' % name)


# Calls the class functions that create the tables of the corresponding models
def create_tables():
    try:
        from project.gateaways.auth_gateaway import UserGateaway
        UserGateaway.create_table()

        from project.models.item_model import Item
        Item.create_table()

        from project.models.inventory_model import Inventory
        Inventory.create_table()

        from project.gateaways.cart_gateaway import CartGateaway
        CartGateaway.create_table()

        from project.models.television_model import Television
        Television.create_table()

        from project.models.tablet_model import Tablet
        Tablet.create_table()

        from project.models.monitor_model import Monitor
        Monitor.create_table()

        from project.models.laptop_model import Laptop
        Laptop.create_table()

        from project.models.desktop_model import Desktop
        Desktop.create_table()

    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()


# Calls the class functions that drop the tables of the corresponding models
def drop_tables():
    try:
        from project.models.television_model import Television
        Television.drop_table()

        from project.models.tablet_model import Tablet
        Tablet.drop_table()

        from project.models.monitor_model import Monitor
        Monitor.drop_table()

        from project.models.laptop_model import Laptop
        Laptop.drop_table()

        from project.models.desktop_model import Desktop
        Desktop.drop_table()

        from project.gateaways.cart_gateaway import CartGateaway
        CartGateaway.drop_table()

        from project.models.inventory_model import Inventory
        Inventory.drop_table()

        from project.models.item_model import Item
        Item.drop_table()

        from project.gateaways.auth_gateaway import UserGateaway
        UserGateaway.drop_table()

    except Exception:
        # Tries dropping the tables again if an exception is raised
        time.sleep(5)
        drop_tables()

def delete_item(**kwargs):
    filters = []

    for key, value in kwargs.items():
        filters.append(str(key) + '=\'' + str(value) + '\'')

    filters = ' AND '.join(filters)

    query = 'DELETE FROM inventories WHERE %s;' % (filters,)
    with connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)

