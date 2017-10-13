
from project.models.item_model import Item
from project.gateways import create_table, drop_table


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
