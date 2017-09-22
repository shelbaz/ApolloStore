
from project.models import connect_to_db
import psycopg2

class Laptop():

    # Class function that creates the 'laptops' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'laptops'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('laptops',))

                # Creates table 'laptops' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE laptops (
                          id UUID PRIMARY KEY,
                          display_size varchar(64),
                          weight decimal,
                          brand varchar(64),
                          price decimal,
                          model varchar(64)
                        );
                        """
                    )

 