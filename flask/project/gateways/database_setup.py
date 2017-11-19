
import time

from project.models.auth import User
from project.models.item import Item
from project.models.inventory import Inventory
from project.models.cart import Cart
from project.models.tablet import Tablet
from project.models.monitor import Monitor
from project.models.laptop import Laptop
from project.models.desktop import Desktop
from project.models.purchase import Purchase
from project.orm import Mapper


def create_tables():
    """Calls the class functions that create the tables of the corresponding models."""
    try:
        Mapper.create_table(User)
        Mapper.create_table(Item)
        Mapper.create_table(Inventory)
        Mapper.create_table(Cart)
        Mapper.create_table(Tablet)
        Mapper.create_table(Monitor)
        Mapper.create_table(Laptop)
        Mapper.create_table(Desktop)
        Mapper.create_table(Purchase)
    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()


def drop_tables():
    """Calls the class functions that drop the tables of the corresponding models."""
    try:
        Mapper.drop_table(Tablet)
        Mapper.drop_table(Monitor)
        Mapper.drop_table(Laptop)
        Mapper.drop_table(Desktop)
        Mapper.drop_table(Cart)
        Mapper.drop_table(Inventory)
        Mapper.drop_table(Purchase)
        Mapper.drop_table(Item)
        Mapper.drop_table(User)
    except Exception:
        # Tries dropping the tables again if an exception is raised
        time.sleep(5)
        drop_tables()
