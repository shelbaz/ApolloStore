
import psycopg2
import time
import os


# Creates a connection to the PostgreSQL using the test database if an argument is passed, and using the dev database if none is passed
def connect_to_db(*args):
    if args:
        with psycopg2.connect(os.getenv('DATABASE_TEST_URL')) as connection:
            return connection
    else:
        with psycopg2.connect(os.getenv('DATABASE_URL')) as connection:
            return connection


# Calls the class functions that create the tables of the corresponding models
def create_tables(*args):
    try:
        from project.models.auth_model import User
        User.create_table(args)

        from project.models.item_model import Item
        Item.create_table(args)

        from project.models.inventory_model import Inventory
        Inventory.create_table(args)

        from project.models.cart_model import Cart
        Cart.create_table(args)

        from project.models.desktop_model import Desktop
        Desktop.create_table(args)

        from project.models.laptop_model import Laptop
        Laptop.create_table(args)

        from project.models.monitor_model import Monitor
        Monitor.create_table(args)

        from project.models.tablet_model import Tablet
        Tablet.create_table(args)

        from project.models.television_model import Television
        Television.create_table(args)

    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()


# Calls the class functions that create the tables of the corresponding models
def drop_tables(*args):
    try:
        from project.models.television_model import Television
        Television.drop_table(args)

        from project.models.tablet_model import Tablet
        Tablet.drop_table(args)

        from project.models.monitor_model import Monitor
        Monitor.drop_table(args)

        from project.models.laptop_model import Laptop
        Laptop.drop_table(args)

        from project.models.desktop_model import Desktop
        Desktop.drop_table(args)

        from project.models.cart_model import Cart
        Cart.drop_table(args)

        from project.models.inventory_model import Inventory
        Inventory.drop_table(args)

        from project.models.item_model import Item
        Item.drop_table(args)

        from project.models.auth_model import User
        User.drop_table(args)

    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        drop_tables()
