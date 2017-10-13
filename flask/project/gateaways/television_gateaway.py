
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class TelevisionGateaway(Item):

    # Adds the television to the database
    @staticmethod
    def insert_into_db(tv):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO televisions (model, type, dimensions) VALUES ('%s', '%s', '%s');"""
                    % (tv.model, tv.type, tv.dimensions))

    @staticmethod
    # Queries the televisions table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN televisions WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN televisions;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        return rows
