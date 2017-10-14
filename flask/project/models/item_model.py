
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db
from project.orm import Mapper


class Item(Mapper):

    name = 'items'

    attributes = {
        'model': 'UUID'
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
    def __init__(self, model):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initializes object attributes
        self.model = model
