
from project.orm import Mapper


class Inventory(Mapper):

    name = 'inventories'

    attributes = {
        'id': 'UUID',
        'model': 'UUID',
        'type': 'varchar(64)',
        'locked': 'boolean'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    # enums = (
    #     {'types': '(\'Desktop\', \'Laptop\', \'Monitor\', \'Tablet\')'}
    # )

    # Constructor that creates inventory
    def __init__(self, id, model, type):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize object attributes
        self.id = id
        self.model = model
        self.type = type
        self.locked = False
