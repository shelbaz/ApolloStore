
from project.models.item_model import Item
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db


class Television(Item):

    attributes = {
        'model': 'UUID',
        'type': 'types',
        'dimensions': 'varchar(64)'
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    enum = {'types': '(\'HD\', \'LED\', \'3D\', \'Smart\')'}

    @staticmethod
    def create_table():
        create_table('televisions', __class__.attributes, __class__.constraints, __class__.enum)

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

    @staticmethod
    def query(**conditions):
        return query_filtered_by('items', 'televisions', **conditions)

    def insert(self):
        super().insert()
        insert_into_db('televisions', __class__.attributes, self)
