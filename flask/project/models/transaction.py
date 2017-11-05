
from project.orm import Mapper


class Transaction(Mapper):

    name = 'transactions'

    attributes = {
        'id': 'UUID',
        'user_id': 'UUID',
        'added_time': 'timestamp'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'FOREIGN KEY (user_id)': 'REFERENCES users (id)'
    }

    # Constructor that creates a new cart
    def __init__(self, id, inventory_id, user_id, added_time):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize the object's attributes
        self.id = id
        self.user_id = user_id
        self.added_time = added_time
