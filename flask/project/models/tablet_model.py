
from project.models import connect_to_db
import psycopg2

class Tablet():

    # Class function that creates the 'tablets' table
    @staticmethod
    def create_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:

                # Searches if there is already a table named 'tablets'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('tablets',))

                # Creates table 'tablets' if it doesn't exist
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
                          os_name varchar(64),
                          camera_info varchar(64),
                          model varchar(64),
                          price decimal
                        );
                        """
                    )

    # Constructor that creates a new tablet
    def __init__(self, id, display_size, dimensions, weight, processor, ram_size, cpu_cores, harddrive_size, battery, brand, os_name, camera_info, model, price):

        # Initialize object attributes
        self.id = id
        self.display_size = display_size
        self.dimensions = dimensions
        self.weight = weight
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.harddrive_size = harddrive_size
        self.battery = battery
        self.brand = brand
        self.os_name = os_name
        self.camera_info = camera_info
        self.price = price
        self.model = model

 