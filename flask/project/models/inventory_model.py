
from project.models import connect_to_db
import psycopg2
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class Inventory():

    # Class function that creates the 'users' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'users'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('inventories',))

                # Creates table 'users' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE inventories (
                          id UUID PRIMARY KEY,
                          model_id varchar(64)
                        );
                        """
                    )

 