
from project.models.item_model import Item
from project.gateways import create_table, drop_table


class Television(Item):

    attributes = {
        'model': 'UUID',
        'types': 'types',
        'dimensions': 'varchar(64)'
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    enums = (
        {'types': '(\'HD\', \'LED\', \'3D\', \'Smart\')'}
    )

    @staticmethod
    def create_table():
        create_table('televisions', attributes, constraints, enums)

    @staticmethod
    def drop_table():
        drop_table('televisions')

    # Constructor that creates a new television
    def __init__(self, model, brand, price, weight, type, dimensions):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.type = type
        self.dimensions = dimensions
