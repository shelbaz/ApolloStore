
from project.models import connect_to_db
import psycopg2

class Cart():

    # Class function that creates the 'carts' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'carts'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('carts',))

                # Creates table 'carts' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE carts (
                          id UUID PRIMARY KEY,
                          inventory_id varchar(64),
                          timestamp date
                        );
                        """
                    )

    # Constructor that creates a new cart
    def __init__(self,id, inventory_id, timestamp):

        # Initialize the object's attributes
        self.id = id
        self.inventory_id = inventory_id
        self.timestamp = timestamp



 