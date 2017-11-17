
from project.gateways import Gateway as gw


class Mapper(object):

    def __init__(self, name, attributes, constraints):
        self._name = name
        self._attributes = attributes
        self._constraints = constraints

    def insert(self):
        if '_item' in dir(self):
            gw.insert_into_db(self._item._name, self._item._attributes, self._item)
        gw.insert_into_db(self._name, self._attributes, self)

    @staticmethod
    def query(*table, **conditions):
        return gw.query_filtered_by(*table, **conditions)

    def update(self, **attributes):
        for key, value in attributes.items():
            setattr(self, key, value)
        gw.update_db(self._name, self._attributes, self)

    def delete(self):
        if '_item' in dir(self):
            gw.delete_from_db(self._item._name)
        key = self._constraints['PRIMARY KEY'].strip('(').strip(')')
        dic = {key: getattr(self, key)}
        gw.delete_from_db(self._name, **dic)

    @staticmethod
    def all_items_query(models):
        return gw.get_all_items(models)

    @staticmethod
    def create_table(table):
        gw.create_table(table.name, table.attributes, table.constraints)

    @staticmethod
    def drop_table(table):
        gw.drop_table(table.name)
