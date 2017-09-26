
from project.models import connect_to_db
import psycopg2
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User():

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

    # Constructor that creates a new user
    def __init__(self, id, first_name, last_name, address, email, phone, admin):

        # Initializes object attributes
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.phone = phone
        self.admin = admin

    # Adds the user to the database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (id, first_name, last_name, address, email, password_hash, phone, admin) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s);"""
                    % (self.id, self.first_name, self.last_name, self.address, self.email, self.password_hash, self.phone, str(self.admin)))

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

        query = """SELECT * FROM users WHERE %s;""" % (filters,)

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        users = []

        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4], row[6], row[7])
            user.password_hash = row[5]
            users.append(user)

        if users:
            return users
        else:
            return None

    # Hashes the password and initializes the user's password_hash attribute
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Verifies that the given password matches the user's password
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # Generate an authentication token
    def generate_auth_token(self, expiration=2592000):
        s = Serializer(os.getenv('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'id': self.id})

    # Verifies the authentication token and returns the user object associated with the token
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(os.getenv('SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query_filtered_by(id=data['id'])[0]
        return user

