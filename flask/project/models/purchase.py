
from project.orm import Mapper


class Purchase(Mapper):

    name = 'purchases'

    attributes = {
        'id': 'UUID',
        'user_id': 'UUID',
        'added_time': 'timestamp',
        'model_id' : 'UUID',
        'type' : 'varchar(64)'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'FOREIGN KEY (user_id)': 'REFERENCES users (id)',
        'FOREIGN KEY (model_id)': 'REFERENCES items (model)'
    }

    # Constructor that creates a new cart
    def __init__(self, id, user_id, added_time, model_id, type):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize the object's attributes
        self.id = id
        self.user_id = user_id
        self.added_time = added_time
        self.model_id = model_id
        self.type = type
