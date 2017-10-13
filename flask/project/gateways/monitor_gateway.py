
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2

class MonitorGateway(Item):

    # Adds the monitor to the database
    @staticmethod
    def insert_into_db(monitor):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO monitors (model, dimensions) VALUES ('%s', '%s');"""
                    % (monitor.model, monitor.dimensions))

    @staticmethod
    # Queries the monitors table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN monitors WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN monitors;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

