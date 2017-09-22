
from project.models import connect_to_db
import psycopg2
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class Television():

    # Class function that creates the 'users' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'users'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('televisions',))

                # Creates table 'users' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TYPE types AS ENUM ('HD', 'LED', '3D', 'Smart');
                        CREATE TABLE televisions (
                          id UUID PRIMARY KEY,
                          type types,
                          price decimal,
                          dimension varchar(64),
                          brand varchar(64),
                          weight varchar(64),
                          model varchar(64) UNIQUE
                        );
                        """
                    )

 