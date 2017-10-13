
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class LaptopGateway(Item):

    # Adds the laptop to the database
    @staticmethod
    def insert_into_db(laptop):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO laptops (model, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera) VALUES ('%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s', '%s');"""
                    % (laptop.model, laptop.display_size, laptop.processor, str(laptop.ram_size), str(laptop.cpu_cores), str(laptop.hd_size), laptop.battery_info, laptop.os, str(laptop.touchscreen), str(laptop.camera)))


    @staticmethod
    # Queries the laptops table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM items NATURAL JOIN laptops WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM items NATURAL JOIN laptops;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
