
from project.models.item_model import Item
from project.gateways import create_table, drop_table


class Tablet(Item):

    attributes = {
        'model': 'UUID',
        'display_size': 'varchar(64)',
        'dimensions': 'varchar(64)',
        'processor': 'varchar(64)',
        'ram_size': 'integer',
        'cpu_cores': 'integer',
        'hd_size': 'integer',
        'battery': 'varchar(64)',
        'os': 'varchar(64)',
        'camera_info': 'varchar(64)'
    }

    constraints = {
        'PRIMARY KEY': '(model)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    @staticmethod
    def create_table():
        create_table('tablets', attributes, constraints)

    @staticmethod
    def drop_table():
        drop_table('tablets')

    # Constructor that creates a new tablet
    def __init__(self, model, brand, price, weight, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.display_size = display_size
        self.dimensions = dimensions
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.battery = battery
        self.os = os
        self.camera_info = camera_info

 