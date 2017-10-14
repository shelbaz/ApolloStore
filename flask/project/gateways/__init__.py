
import psycopg2
import time
import os
from flask import current_app
import traceback
from project import logger


# Creates a connection to the PostgreSQL using the test database if an argument is passed, and using the dev database if none is passed
def connect_to_db():
    if current_app.config['TESTING']:
        with psycopg2.connect(os.getenv('DATABASE_TEST_URL')) as connection:
            return connection
    else:
        with psycopg2.connect(os.getenv('DATABASE_URL')) as connection:
            return connection


def insert_into_db(table, attributes, obj):

    types_with_no_quotes = ['integer', 'decimal', 'boolean']

    query = 'INSERT INTO %s (' % table

    currently_first_attribute = True

    for key in attributes.keys():
        if currently_first_attribute:
            currently_first_attribute = False
        else:
            query += ', '
        query += key

    query += ') VALUES ('

    currently_first_attribute = True

    for key, value in attributes.items():
        if currently_first_attribute:
            currently_first_attribute = False
        else:
            query += ', '
        if value in types_with_no_quotes:
            query += str(getattr(obj, key))
        else:
            query += '\'%s\'' % str(getattr(obj, key))

    query += ');'

    with connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)


def query_filtered_by(*tables, **conditions):

    filters = []

    for key, value in conditions.items():
        filters.append(str(key) + '=\'' + str(value) + '\'')

    filters = ' AND '.join(filters)

    # Joins the tables if multiple are given
    tables = ' NATURAL JOIN '.join(tables)

    if filters:
        query = 'SELECT * FROM %s WHERE %s;' % (tables, filters)
    else:
        query = 'SELECT * FROM %s;' % tables

    with connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    if rows:
        return rows
    else:
        return None


def get_inventory_count(table, model):
    try:
        query = 'SELECT COUNT(*) FROM inventories NATURAL JOIN (SELECT * FROM %s WHERE model=\'%s\') AS x;' % (table, model)
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()
        return count[0]
    except Exception:
        logger.error(traceback.format_exc())


def delete_from_db(*tables, **conditions):

    filters = []

    for key, value in conditions.items():
        filters.append(str(key) + '=\'' + str(value) + '\'')

    filters = ' AND '.join(filters)

    for table in tables:
        query = 'DELETE FROM %s WHERE %s;' % (table, filters)

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)


def create_table(name, attributes, constraints):
    # Using the 'with' statement automatically commits and closes database connections
    with connect_to_db() as connection:
        with connection.cursor() as cursor:

            # Searches if there is already a table with the same name
            cursor.execute('SELECT * FROM information_schema.tables WHERE table_name=\'%s\'' % name)

            query = 'CREATE TABLE %s (' % name

            # Adds attributes
            for key, value in attributes.items():
                query += '%s %s, ' % (key, value)

            currently_first_constraint = True

            # Adds constraints
            for key, value in constraints.items():
                if currently_first_constraint:
                    query += '%s %s' % (key, value)
                    currently_first_constraint = False
                else:
                    query += ', %s %s' % (key, value)

            query += ');'

            if not bool(cursor.rowcount):
                cursor.execute(query)


def drop_table(name):
    # Using the 'with' statement automatically commits and closes database connections
    with connect_to_db() as connection:
        with connection.cursor() as cursor:
            # Searches if there is already a table with the same name
            cursor.execute('SELECT * FROM information_schema.tables WHERE table_name=\'%s\'' % name)

            # Deletes table if it exists
            if bool(cursor.rowcount):
                cursor.execute('DROP TABLE %s;' % name)

from project.models.auth_model import User
from project.models.item_model import Item
from project.models.inventory_model import Inventory
from project.models.cart_model import Cart
from project.models.tablet_model import Tablet
from project.models.monitor_model import Monitor
from project.models.laptop_model import Laptop
from project.models.desktop_model import Desktop
from project.orm import Mapper


# Calls the class functions that create the tables of the corresponding models
def create_tables():
    try:
        Mapper.create_table(User)
        Mapper.create_table(Item)
        Mapper.create_table(Inventory)
        Mapper.create_table(Cart)
        Mapper.create_table(Tablet)
        Mapper.create_table(Monitor)
        Mapper.create_table(Laptop)
        Mapper.create_table(Desktop)
    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()


# Calls the class functions that drop the tables of the corresponding models
def drop_tables():
    try:
        Mapper.drop_table(Tablet)
        Mapper.drop_table(Monitor)
        Mapper.drop_table(Laptop)
        Mapper.drop_table(Desktop)
        Mapper.drop_table(Cart)
        Mapper.drop_table(Inventory)
        Mapper.drop_table(Item)
        Mapper.drop_table(User)
    except Exception:
        # Tries dropping the tables again if an exception is raised
        time.sleep(5)
        drop_tables()
