
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db
from project.orm import Mapper


class Cart(Mapper):

    name = 'carts'

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

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize the object's attributes
        self.id = id
        self.inventory_id = inventory_id
        self.user_id = user_id
        self.added_time = added_time
