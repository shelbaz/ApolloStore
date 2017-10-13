
from project.gateways import create_table, drop_table, query_filtered_by, insert_into_db, delete_from_db


class Inventory(object):

    attributes = {
        'id': 'UUID',
        'model': 'UUID'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'FOREIGN KEY (model)': 'REFERENCES items (model)'
    }

    @staticmethod
    def create_table():
        create_table('inventories', __class__.attributes, __class__.constraints)

    @staticmethod
    def drop_table():
        drop_table('inventories')

    # Constructor that creates inventory
    def __init__(self, id, model):

        # Initialize object attributes
        self.id = id
        self.model = model

    @staticmethod
    def query(**conditions):
        return query_filtered_by('inventories', **conditions)

    def insert(self):
        insert_into_db('inventories', __class__.attributes, self)

    def delete(self):
        delete_from_db('inventories', id=self.id)
