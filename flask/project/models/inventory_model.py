
from project.models import connect_to_db
import psycopg2

    # Class function that creates the 'inventories' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'inventories'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('inventories',))

                # Creates table 'inventories' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE inventories (
                          id UUID PRIMARY KEY,
                          model_id varchar(64)
                        );
                        """
                    )

    # Constructor that creates inventory
    def __init__(self, id, model_id):
        # Initialize object attributes
        self.id = id
        self.model_id = model_id

