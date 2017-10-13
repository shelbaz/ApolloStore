
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class TabletGateaway(Item):

    # Adds the tablet to the database
    @staticmethod
    def insert_into_db(tablet):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO tablets (model, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info) VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s');"""
                    % (tablet.model, tablet.display_size, tablet.dimensions, tablet.processor, str(tablet.ram_size), str(tablet.cpu_cores), str(tablet.hd_size), tablet.battery, tablet.os, tablet.camera_info))

    @staticmethod
    # Queries the tablets table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN tablets WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN tablets;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
