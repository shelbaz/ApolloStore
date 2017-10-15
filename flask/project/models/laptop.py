
from project.models.item import Item
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db
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
    def __init__(self, model, brand, price, weight, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera):

        Mapper.__init__(self, __class__.name, __class__.attributes, __class__.constraints)

        # Creates the Item object
        self._item = Item(model)

        # Initialize object attributes
        self.model = model
        self.brand = brand
        self.price = price
        self.weight = weight
        self.display_size = display_size
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.battery_info = battery_info
        self.os = os
        self.touchscreen = touchscreen
        self.camera = camera
