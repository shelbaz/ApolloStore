
from project.models import connect_to_db
import psycopg2


class Item(object):

    # Constructor that creates a new item
    def __init__(self, model, brand, price, weight):

        # Initializes object attributes
        self.model = model
        self.brand = brand
        self.price = price
        self.weight = weight
