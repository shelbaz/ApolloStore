
from project.models.item_model import Item
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db


class Monitor(Item):

    attributes = {
        'model': 'UUID',
        'dimensions': 'varchar(64)'
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    @staticmethod
    def create_table():
        create_table('monitors', __class__.attributes, __class__.constraints)

    @staticmethod
    def drop_table():
        drop_table('monitors')

    # Constructor that creates a new monitor
    def __init__(self, model, brand, price, weight, dimensions):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.dimensions = dimensions

    @staticmethod
    def query(**conditions):
        return query_filtered_by('items', 'monitors', **conditions)

    def insert(self):
        super().insert()
        insert_into_db('monitors', __class__.attributes, self)

    def delete(self):
        super().delete()
        delete_from_db('monitors', id=self.id)
