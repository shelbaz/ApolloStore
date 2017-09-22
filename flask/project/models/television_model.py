
from project.models import connect_to_db
import psycopg2

class Television():

    # Class function that creates the 'televisions' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'televisions'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('televisions',))

                # Creates table 'televisions' if it doesn't exist
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

 