
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
        from project.gateaways.auth_gateaway import UserGateaway
        UserGateaway.create_table()

        from project.gateaways.item_gateaway import ItemGateaway
        ItemGateaway.create_table()

        from project.gateaways.inventory_gateaway import InventoryGateaway
        InventoryGateaway.create_table()

        from project.gateaways.cart_gateaway import CartGateaway
        CartGateaway.create_table()

        from project.gateaways.desktop_gateaway import DesktopGateaway
        DesktopGateaway.create_table()

        from project.gateaways.laptop_gateaway import LaptopGateaway
        LaptopGateaway.create_table()

        from project.gateaways.monitor_gateaway import MonitorGateaway
        MonitorGateaway.create_table()

        from project.gateaways.tablet_gateaway import TabletGateaway
        TabletGateaway.create_table()

        from project.gateaways.television_gateaway import TelevisionGateaway
        TelevisionGateaway.create_table()

    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()


# Calls the class functions that drop the tables of the corresponding models
def drop_tables():
    try:
        from project.gateaways.television_gateaway import TelevisionGateaway
        TelevisionGateaway.drop_table()

        from project.gateaways.tablet_gateaway import TabletGateaway
        TabletGateaway.drop_table()

        from project.gateaways.monitor_gateaway import MonitorGateaway
        MonitorGateaway.drop_table()

        from project.gateaways.laptop_gateaway import LaptopGateaway
        LaptopGateaway.drop_table()

        from project.gateaways.desktop_gateaway import DesktopGateaway
        DesktopGateaway.drop_table()

        from project.gateaways.cart_gateaway import CartGateaway
        CartGateaway.drop_table()

        from project.gateaways.inventory_gateaway import InventoryGateaway
        InventoryGateaway.drop_table()

        from project.gateaways.item_gateaway import ItemGateaway
        ItemGateaway.drop_table()

        from project.gateaways.auth_gateaway import UserGateaway
        UserGateaway.drop_table()

    except Exception:
        # Tries dropping the tables again if an exception is raised
        time.sleep(5)
        drop_tables()

def delete_item(type, model):
    query = """
        DELETE FROM " + type + " WHERE model='" + model + "';
    """
    query2 = """
        DELETE FROM items WHERE model='" + model + "';
    """
    with connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            if type != 'inventories':
                cursor.execute(query2)

                