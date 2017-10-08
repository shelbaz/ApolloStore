
from project.models import connect_to_db
import psycopg2
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class UserGateaway():

    # Class function that creates the 'users' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'users'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('users',))

                # Creates table 'users' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE users (
                          id UUID PRIMARY KEY,
                          first_name varchar(64),
                          last_name varchar(64),
                          address varchar(256),
                          email varchar(128) UNIQUE,
                          password_hash varchar(256),
                          phone varchar(64),
                          admin boolean
                        );
                        """
                    )

    # Class function that deletes the 'users' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'users'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('users',))

                # Deletes table 'users' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE users;')

    # Adds the user to the database
    @staticmethod
    def insert_into_db(user):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (id, first_name, last_name, address, email, password_hash, phone, admin) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s);"""
                    % (user.id, user.first_name, user.last_name, user.address, user.email, user.password_hash, user.phone, str(user.admin)))

    # Queries the users table with the filters given as parameters (only equality filters)
    @staticmethod
    def query_filtered_by(**kwargs):
        """
        Example usage: User.query_filtered_by(first_name='Elon', last_name='Bean')
        will return a list of User object with the conditions given as parameters
        """

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = """SELECT * FROM users WHERE %s;""" % (filters,)
        else:
            query = """SELECT * FROM users;"""

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None



