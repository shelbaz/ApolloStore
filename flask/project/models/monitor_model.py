
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Monitor(Item):

    # Class function that creates the 'monitors' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'monitors'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('monitors',))

                # Creates table 'monitors' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE monitors (
                          model UUID PRIMARY KEY,
                          dimensions varchar(64),
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Constructor that creates a new monitor
    def __init__(self, model, price, weight, brand, dimensions):

        # Creates the Item object
        super().__init__(model, price, weight, brand)

        # Initialize object attributes
        self.model = model
        self.dimensions = dimensions
