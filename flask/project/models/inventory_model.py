
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db
from project.orm import Mapper


class Inventory(Mapper):

    name = 'inventories'

    attributes = {
        'id': 'UUID',
        'model': 'UUID'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    # Constructor that creates inventory
    def __init__(self, id, model):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize object attributes
        self.id = id
        self.model = model
