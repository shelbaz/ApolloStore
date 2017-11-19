from project.gateways import insert_into_db, query_filtered_by, delete_from_db, create_table, drop_table, update_db, count_rows, get_all_items

class Mapper(object):

    def __init__(self, name, attributes, constraints):
        self._name = name
        self._attributes = attributes
        self._constraints = constraints

    def insert(self):
        if '_item' in dir(self):
            insert_into_db(self._item._name, self._item._attributes, self._item)
        insert_into_db(self._name, self._attributes, self)

    @staticmethod
    def query(*table, **conditions):
        return query_filtered_by(*table, **conditions)

    @staticmethod
    def order_by(attribute, *table):
        return query_filtered_by_order(attribute,*table)

    def update(self, **attributes):
        for key, value in attributes.items():
            setattr(self, key, value)
        update_db(self._name, self._attributes, self)

    def delete(self):
        if '_item' in dir(self):
            delete_from_db(self._item._name)
        key = self._constraints['PRIMARY KEY'].strip('(').strip(')')
        dic = {key: getattr(self, key)}
        delete_from_db(self._name, **dic)

    @staticmethod
    def count_rows(table, user_id):
        return count_rows(table.name, user_id)

    @staticmethod
    def all_items_query(models):
        return get_all_items(models)

    @staticmethod
    def create_table(table):
        create_table(table.name, table.attributes, table.constraints)

    @staticmethod
    def drop_table(table):
        drop_table(table.name)
