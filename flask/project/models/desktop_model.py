
from project.models.item_model import Item
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db


class Desktop(Item):

    attributes = {
        'model': 'UUID',
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

    @staticmethod
    def create_table():
        create_table('desktops', __class__.attributes, __class__.constraints)

    @staticmethod
    def drop_table():
        drop_table('desktops')

    # Constructor that creates a new desktop
    def __init__(self, model, brand, price, weight, processor, ram_size, cpu_cores, hd_size, dimensions):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.dimensions = dimensions
 
    @staticmethod 
    def query(**conditions):
        return query_filtered_by('items', 'desktops', **conditions)

    def insert(self):
        super().insert()
        insert_into_db('desktops', __class__.attributes, self)

    def delete(self):
        super().delete()
        delete_from_db('desktops', model=self.model)
