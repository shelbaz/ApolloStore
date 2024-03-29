
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

    # Constructor that creates inventory
    def __init__(self, id, model, type, locked=False):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize object attributes
        self.id = id
        self.model = model
        self.type = type
        self.locked = locked
