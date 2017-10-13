
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2

class DesktopGateway(Item):

    # Adds the desktop to the database
    @staticmethod
    def insert_into_db(desktop):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO desktops (model, processor, ram_size, cpu_cores, hd_size, dimensions) VALUES ('%s', '%s', %s, %s, %s, '%s');"""
                    % (desktop.model, desktop.processor, str(desktop.ram_size), str(desktop.cpu_cores), str(desktop.hd_size), desktop.dimensions))

    @staticmethod
    # Queries the desktops table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN desktops WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN desktops;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
