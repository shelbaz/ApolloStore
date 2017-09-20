
from project.models import connect_to_db
import psycopg2
import uuid


class User():

    # Class function that creates this table
    @staticmethod
    def create_table():
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
                          email varchar(128),
                          phone varchar(64),
                          admin boolean
                        );
                        """
                    )

    # Constructor that creates a new user
    def __init__(self, first_name, last_name, address, email, phone, admin):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (id, first_name, last_name, address, email, phone, admin) VALUES (
                      """ + uuid.uuid4() + """,
                      """ + first_name + """,
                      """ + last_name + """,
                      """ + address + """,
                      """ + email + """,
                      """ + phone + """,
                      """ + admin + """
                    );
                    """
                )
