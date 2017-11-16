
from project.models.item import Item
from project.orm import Mapper
from project import identity_map

class Desktop(Item, Mapper):

    name = 'desktops'

    attributes = {
        'model': 'UUID',
        'brand': 'varchar(64)',
        'price': 'decimal',
        'weight': 'decimal',
        'processor': 'varchar(64)',
        'ram_size': 'integer',
        'cpu_cores': 'integer',
        'hd_size': 'integer',
        'dimensions': 'varchar(64)',
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    # Constructor that creates a new desktop
    def __init__(self, model, brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):

        Mapper.__init__(self, __class__.name, __class__.attributes, __class__.constraints)

        # Creates the Item object
        self._item = Item(model)

        # Initialize object attributes
        self.model = model
        self.brand = brand
        self.price = price
        self.weight = weight
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.dimensions = dimensions

    def serialize(self):
        #  return {
        #     'brand': str(self.brand),
        #     'price': str(self.price)
        # }
        return {
            'brand': str(self.brand),
            'price': str(self.price),
            'weight': str(self.weight),
            'processor': str(self.processor),
            'ram_size': str(self.ram_size),
            'cpu_cores': str(self.cpu_cores),
            'hd_size': str(self.hd_size),
            'dimensions': str(self.dimensions)
        }