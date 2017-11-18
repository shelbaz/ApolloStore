
import traceback
import os

import psycopg2
from flask import current_app

from project import logger


class Gateway:

    @staticmethod
    def connect_to_db():
        """Creates a connection to the database using the test database if an argument is passed, and using the dev database if none is passed."""
        if current_app.config['TESTING']:
            with psycopg2.connect(os.getenv('DATABASE_TEST_URL')) as connection:
                return connection
        else:
            with psycopg2.connect(os.getenv('DATABASE_URL')) as connection:
                return connection

    @staticmethod
    def insert_into_db(table, attributes, obj):
        """Inserts a record in the database."""
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

        with Gateway.connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

    @staticmethod
    def query_filtered_by(*tables, **conditions):
        """Queries a list of naturally joined tables with optional conditions."""
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

        with Gateway.connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return []

    @staticmethod
    def get_all_items(models):
        """Returns all items inventory rows corresponding to models from a list of models."""
        filters = []

        for model in models:
            filters.append('model=\'' + str(model) + '\'')

        filters = ' OR '.join(filters)

        items = '((select model, brand, price from tablets) union (select model, brand, price from laptops) union (select model, brand, price from desktops) union (select model, brand, price from monitors)) as X'

        if filters:
            query = 'SELECT * FROM %s WHERE %s;' % (items, filters)
        else:
            query = 'SELECT * FROM %s;' % items

        with Gateway.connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

    @staticmethod
    def delete_from_db(*tables, **conditions):
        """Deletes entries in a table or natural joins of tables with the conditions provided."""
        filters = []

        for key, value in conditions.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        for table in tables:
            query = 'DELETE FROM %s WHERE %s;' % (table, filters)

            with Gateway.connect_to_db() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)

    @staticmethod
    def update_db(table, attributes, obj):
        """Updates an entry in the database with the attributes provided."""
        types_with_no_quotes = ['integer', 'decimal', 'boolean']
        if(table == 'inventories'):
            whereStatement = 'id'
            id = obj.id
        else:
            whereStatement = 'model'
            id=obj.model
        query = 'UPDATE %s SET ' % table

        currently_first_attribute = True

        for key, value in attributes.items():
            if currently_first_attribute:
                currently_first_attribute = False
            else:
                query += ', '
            if value in types_with_no_quotes:
                query += str(key) + '='+ str(getattr(obj, key))
            else:
                query += str(key) + '=\'' + str(getattr(obj, key)) + '\''

        where_condition = whereStatement + '=\'' + str(id) + '\''

        query+= ' WHERE %s' % where_condition + ';'
        with Gateway.connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

    @staticmethod
    def create_table(name, attributes, constraints):
        """Creates a table in the database with the given attributes and constraints."""
        with Gateway.connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table with the same name
                cursor.execute('SELECT * FROM information_schema.tables WHERE table_name=\'%s\'' % name)

                query = 'CREATE TABLE %s (' % name

                for key, value in attributes.items():
                    query += '%s %s, ' % (key, value)

                currently_first_constraint = True

                for key, value in constraints.items():
                    if currently_first_constraint:
                        query += '%s %s' % (key, value)
                        currently_first_constraint = False
                    else:
                        query += ', %s %s' % (key, value)

                query += ');'

                if not bool(cursor.rowcount):
                    cursor.execute(query)

    @staticmethod
    def drop_table(name):
        """Drops a table from the database with the given name."""
        with Gateway.connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table with the same name
                cursor.execute('SELECT * FROM information_schema.tables WHERE table_name=\'%s\'' % name)

                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE %s;' % name)
