
from project.models.item_model import Item
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db


class Laptop(Item):

    attributes = {
        'model': 'UUID',
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

    @staticmethod
    def create_table():
        create_table('laptops', __class__.attributes, __class__.constraints)

    @staticmethod
    def drop_table():
        drop_table('laptops')

    # Constructor that creates a new laptop
    def __init__(self, model, brand, price, weight, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.display_size = display_size
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.battery_info = battery_info
        self.os = os
        self.touchscreen = touchscreen
        self.camera = camera

    @staticmethod
    def query(**conditions):
        return query_filtered_by('items', 'laptops', **conditions)

    def insert(self):
        super().insert()
        insert_into_db('laptops', __class__.attributes, self)
