
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


# Calls the class functions that create the tables of the corresponding models
def create_tables():
    try:
        from project.gateways.auth_gateway import UserGateway
        UserGateway.create_table()

        from project.gateways.item_gateway import ItemGateway
        ItemGateway.create_table()

        from project.gateways.inventory_gateway import InventoryGateway
        InventoryGateway.create_table()

        from project.gateways.cart_gateway import CartGateway
        CartGateway.create_table()

        from project.gateways.desktop_gateway import DesktopGateway
        DesktopGateway.create_table()

        from project.gateways.laptop_gateway import LaptopGateway
        LaptopGateway.create_table()

        from project.gateways.monitor_gateway import MonitorGateway
        MonitorGateway.create_table()

        from project.gateways.tablet_gateway import TabletGateway
        TabletGateway.create_table()

        from project.gateways.television_gateway import TelevisionGateway
        TelevisionGateway.create_table()

    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()


# Calls the class functions that drop the tables of the corresponding models
def drop_tables():
    try:
        from project.gateways.television_gateway import TelevisionGateway
        TelevisionGateway.drop_table()

        from project.gateways.tablet_gateway import TabletGateway
        TabletGateway.drop_table()

        from project.gateways.monitor_gateway import MonitorGateway
        MonitorGateway.drop_table()

        from project.gateways.laptop_gateway import LaptopGateway
        LaptopGateway.drop_table()

        from project.gateways.desktop_gateway import DesktopGateway
        DesktopGateway.drop_table()

        from project.gateways.cart_gateway import CartGateway
        CartGateway.drop_table()

        from project.gateways.inventory_gateway import InventoryGateway
        InventoryGateway.drop_table()

        from project.gateways.item_gateway import ItemGateway
        ItemGateway.drop_table()

        from project.gateways.auth_gateway import UserGateway
        UserGateway.drop_table()

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

