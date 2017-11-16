
from project.models.item import Item
from project.orm import Mapper


class Laptop(Item, Mapper):

    name = 'laptops'

    attributes = {
        'model': 'UUID',
        'brand': 'varchar(64)',
        'price': 'decimal',
        'weight': 'decimal',
        'display_size': 'varchar(64)',
        'processor': 'varchar(64)',
        'ram_size': 'integer',
        'cpu_cores': 'integer',
        'hd_size': 'integer',
        'battery_info': 'varchar(64)',
        'os': 'varchar(64)',
        'touchscreen': 'boolean',
        'camera': 'boolean'
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    # Constructor that creates a new laptop
    def __init__(self, **attributes):

        Mapper.__init__(self, __class__.name, __class__.attributes, __class__.constraints)

        # Creates the Item object
        self._item = Item(attributes['model'])

        # Initialize object attributes
        self.model = attributes['model']
        self.brand = attributes['brand']
        self.price = attributes['price']
        self.weight = attributes['weight']
        self.display_size = attributes['display_size']
        self.processor = attributes['processor']
        self.ram_size = attributes['ram_size']
        self.cpu_cores = attributes['cpu_cores']
        self.hd_size = attributes['hd_size']
        self.battery_info = attributes['battery_info']
        self.os = attributes['os']
        self.touchscreen = attributes['touchscreen']
        self.camera = attributes['camera']
