
import psycopg2
import time


# Creates a connection to the PostgreSQL
def connect_to_db():
    with psycopg2.connect('postgresql://postgres:postgres@postgres:5432/db_dev') as connection:
        return connection


# Calls the class functions that create the tables of the corresponding models
def create_tables():
    try:
        from project.models.auth_model import User
        User.create_table()

        from project.models.item_model import Item
        Item.create_table()

        from project.models.inventory_model import Inventory
        Inventory.create_table()

        from project.models.cart_model import Cart
        Cart.create_table()

        from project.models.desktop_model import Desktop
        Desktop.create_table()

        from project.models.laptop_model import Laptop
        Laptop.create_table()

        from project.models.monitor_model import Monitor
        Monitor.create_table()

        from project.models.tablet_model import Tablet
        Tablet.create_table()

        from project.models.television_model import Television
        Television.create_table()

    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()

    # Calls the class functions that create the tables of the corresponding models
    def drop_tables():
        try:
            from project.models.auth_model import User
            User.drop_table()

            from project.models.item_model import Item
            Item.drop_table()

            from project.models.inventory_model import Inventory
            Inventory.drop_table()

            from project.models.cart_model import Cart
            Cart.drop_table()

            from project.models.desktop_model import Desktop
            Desktop.drop_table()

            from project.models.laptop_model import Laptop
            Laptop.drop_table()

            from project.models.monitor_model import Monitor
            Monitor.drop_table()

            from project.models.tablet_model import Tablet
            Tablet.drop_table()

            from project.models.television_model import Television
            Television.drop_table()

        except Exception:
            # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
            time.sleep(5)
            drop_tables()
