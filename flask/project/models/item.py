
from project.orm import Mapper


class Item(Mapper):

    name = 'items'

    attributes = {
        'model': 'UUID'
    }

    constraints = {
        'PRIMARY KEY': '(model)'
    }

    # Constructor that creates a new item
    def __init__(self, model):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initializes object attributes
        self.model = model
