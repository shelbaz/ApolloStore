
from project.orm import Mapper


class Purchases(Mapper):

    name = 'purchases'

    attributes = {
        'id': 'UUID',
        'user_id': 'UUID',
        'added_time': 'timestamp',
        'model_id' : 'UUID'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'FOREIGN KEY (user_id)': 'REFERENCES users (id)',
        'FOREIGN KEY (modelID)': 'REFERENCES inventories (model)'
    }

    # Constructor that creates a new cart
    def __init__(self, id, inventory_id, user_id, added_time, model_id):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize the object's attributes
        self.id = id
        self.user_id = user_id
        self.added_time = added_time
        self.model_id = model_id
