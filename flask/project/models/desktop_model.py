
from project.models import connect_to_db
import psycopg2

class Desktop():

    # Class function that creates the 'desktops' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'desktops'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('desktops',))

                # Creates table 'desktops' if it doesn't exist
                if not bool(cursor.rowcount):
                    cursor.execute(
                        """
                        CREATE TABLE desktops (
                          id UUID PRIMARY KEY,
                          processor varchar(64),
                          ram_size integer,
                          weight decimal,
                          cpu_cores integer,
                          harddrive_size integer,
                          brand varchar(64),
                          price decimal,
                          model varchar(64)
                        );
                        """
                    )

    # Constructor that creates a new desktop
    def __init__(self, id, processor, ram_size, weight, cpu_cores, harddrive_size, brand, price, model):

        # Initialize object attributes
        self.id = id
        self.processor = processor
        self.ram_size = ram_size
        self.weight = weight
        self.cpu_cores = cpu_cores
        self.harddrive_size = harddrive_size
        self.brand = brand
        self.price = price
        self.model = model


 