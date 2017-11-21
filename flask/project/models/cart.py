
from project.orm import Mapper


class Cart(Mapper):

    name = 'carts'

    attributes = {
        'id': 'UUID',
        'inventory_id': 'UUID',
        'model': 'UUID',
        'user_id': 'UUID',
        'expiry_time': 'integer'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'UNIQUE': '(inventory_id)',
        'FOREIGN KEY (inventory_id)': 'REFERENCES inventories (id)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)',
        'FOREIGN KEY (user_id)': 'REFERENCES users (id)'
    }

    # Constructor that creates a new cart
    def __init__(self, id, inventory_id, model, user_id, expiry_time):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initialize the object's attributes
        self.id = id
        self.inventory_id = inventory_id
        self.model = model
        self.user_id = user_id
        self.expiry_time = expiry_time
