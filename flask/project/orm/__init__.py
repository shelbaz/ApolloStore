
from project.gateways import insert_into_db, query_filtered_by, delete_from_db, create_table, drop_table


class Mapper(object):

    def __init__(self, name, attributes, constraints, *extra):
        self._name = name
        self._attributes = attributes
        self._constraints = constraints
        self._extra = extra

    def insert(self):
        # if self.__class__.__mro__[1].__name__ == 'Item':
        if '_item' in dir(self):
            insert_into_db(self._item._name, self._item._attributes, self._item)
        insert_into_db(self._name, self._attributes, self)

    @staticmethod
    def query(*table, **conditions):
        return query_filtered_by(*table, **conditions)

    def update(self):
        pass

    def delete(self):
        if '_item' in dir(self):
            delete_from_db(self._item._name)
        key = self._constraints['PRIMARY KEY'].strip('(').strip(')')
        dic = {key: getattr(self, key)}
        delete_from_db(self._name, **dic)

    @staticmethod
    def create_table(table):
        create_table(table.name, table.attributes, table.constraints)

    @staticmethod
    def drop_table(table):
        drop_table(table.name)
