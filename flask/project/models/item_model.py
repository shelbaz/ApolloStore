
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db


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

    @staticmethod
    def query(**conditions):
        return query_filtered_by('items', **conditions)

    def insert(self):
        insert_into_db('items', __class__.attributes, self)

    def delete(self):
        delete_from_db('items', model=self.model)
