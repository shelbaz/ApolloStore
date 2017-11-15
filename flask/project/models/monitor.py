
from project.models.item import Item
from project.orm import Mapper


class Monitor(Item, Mapper):

    name = 'monitors'

    attributes = {
        'model': 'UUID',
        'brand': 'varchar(64)',
        'price': 'decimal',
        'weight': 'decimal',
        'dimensions': 'varchar(64)'
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    # Constructor that creates a new monitor
    def __init__(self, model, brand, price, weight, dimensions):

        Mapper.__init__(self, __class__.name, __class__.attributes, __class__.constraints)

        # Creates the Item object
        self._item = Item(model)

        # Initialize object attributes
        self.model = model
        self.brand = brand
        self.price = price
        self.weight = weight
        self.dimensions = dimensions
