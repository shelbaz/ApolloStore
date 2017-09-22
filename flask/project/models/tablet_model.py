
from project.models import connect_to_db
import psycopg2
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class Tablet():

    # Class function that creates the 'users' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'users'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('tablets',))

                # Creates table 'users' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE tablets (
                          id UUID PRIMARY KEY,
                          display_size varchar(64),
                          dimensions varchar(64),
                          weight decimal,
                          processor varchar(64),
                          ram_size integer,
                          cpu_cores integer,
                          harddrive_size integer,
                          battery varchar(64),
                          brand varchar(64),
                          OS varchar(64),
                          camera_info varchar(64),
                          model varchar(64),
                          price decimal
                        );
                        """
                    )

 