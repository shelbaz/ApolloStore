
import psycopg2
import os
from flask import current_app


# Creates a connection to the PostgreSQL using the test database if an argument is passed, and using the dev database if none is passed
def connect_to_db():
    if current_app.config['TESTING']:
        with psycopg2.connect(os.getenv('DATABASE_TEST_URL')) as connection:
            return connection
    else:
        with psycopg2.connect(os.getenv('DATABASE_URL')) as connection:
            return connection
