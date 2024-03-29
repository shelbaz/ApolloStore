from project.models.item import Item
from project.orm import Mapper

class Tablet(Item, Mapper):

    name = 'tablets'

    attributes = {
        'model': 'UUID',
        'brand': 'varchar(64)',
        'price': 'decimal',
        'weight': 'decimal',
        'display_size': 'varchar(64)',
        'dimensions': 'varchar(64)',
        'processor': 'varchar(64)',
        'ram_size': 'integer',
        'cpu_cores': 'integer',
        'hd_size': 'integer',
        'battery': 'varchar(64)',
        'os': 'varchar(64)',
        'camera_info': 'varchar(64)',
        'hide': 'boolean'
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    # Constructor that creates a new tablet
    def __init__(self, model, brand, price, weight, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info, hide=False):

        Mapper.__init__(self, __class__.name, __class__.attributes, __class__.constraints)

        # Creates the Item object
        self._item = Item(model)

        # Initialize object attributes
        self.model = model
        self.brand = brand
        self.price = price
        self.weight = weight
        self.display_size = display_size
        self.dimensions = dimensions
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.battery = battery
        self.os = os
        self.camera_info = camera_info
        self.hide = hide

    def serialize(self):
        return {
            'model': str(self.model),
            'brand': str(self.brand),
            'price': str(self.price),
            'weight': str(self.weight),
            'display_size': str(self.display_size),
            'processor': str(self.processor),
            'ram_size': str(self.ram_size),
            'cpu_cores': str(self.cpu_cores),
            'hd_size': str(self.hd_size),
            'battery': str(self.battery),
            'os': str(self.os),
            'camera_info': str(self.camera_info),
            'dimensions': str(self.dimensions)
        }
