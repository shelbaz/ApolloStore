
from project.orm import Mapper


class Item(Mapper):

    name = 'items'

    attributes = {
        'model': 'UUID',
        'brand': 'varchar(64)',
        'price': 'decimal'
    }

    constraints = {
        'PRIMARY KEY': '(model)'
    }

    # Constructor that creates a new item
    def __init__(self, model, brand, price):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initializes object attributes
        self.model = model
        self.brand = brand
        self.price = price
