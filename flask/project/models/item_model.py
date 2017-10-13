
from project.gateaways import create_table, drop_table


class Item(object):

    attributes = {
        'model': 'UUID',
        'brand': 'varchar(64)',
        'price': 'decimal',
        'weight': 'decimal'
    }

    constraints = {
        'PRIMARY KEY': '(model)'
    }

    @staticmethod
    def create_table():
        create_table('items', __class__.attributes, __class__.constraints)

    @staticmethod
    def drop_table():
        drop_table('items')

    # Constructor that creates a new item
    def __init__(self, model, brand, price, weight):

        # Initializes object attributes
        self.model = model
        self.brand = brand
        self.price = price
        self.weight = weight
