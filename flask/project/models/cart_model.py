
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db


class Cart(object):

    attributes = {
        'id': 'UUID',
        'inventory_id': 'UUID',
        'user_id': 'UUID',
        'added_time': 'timestamp'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'UNIQUE': '(inventory_id)',
        'FOREIGN KEY (inventory_id)': 'REFERENCES inventories (id)',
        'FOREIGN KEY (user_id)': 'REFERENCES users (id)'
    }

    @staticmethod
    def create_table():
        create_table('carts', __class__.attributes, __class__.constraints)

    @staticmethod
    def drop_table():
        drop_table('carts')

    # Constructor that creates a new cart
    def __init__(self, id, inventory_id, user_id, added_time):

        # Initialize the object's attributes
        self.id = id
        self.inventory_id = inventory_id
        self.user_id = user_id
        self.added_time = added_time

    @staticmethod
    def query(**conditions):
        return query_filtered_by('carts', **conditions)

    def insert(self):
        insert_into_db('carts', __class__.attributes, self)
