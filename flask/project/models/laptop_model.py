
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
                          processor varchar(64),
                          ram_size integer,
                          weight decimal,
                          cpu_cores integer,
                          harddrive_size integer,
                          battery_info varchar(64),
                          os_name varchar(64),
                          touchscreen boolean,
                          camera boolean,
                          brand varchar(64),
                          price decimal,
                          model varchar(64)
                        );
                        """
                    )

    # Constructor that creates a new laptop
    def __init__(self, id, display_size, processor, ram_size, weight, cpu_cores, harddrive_size, battery_info, os_name, touchscreen, camera, brand, price, model):

        # Initialize object attributes
        self.id = id
        self.display_size = display_size
        self.processor = processor
        self.ram_size = ram_size
        self.weight = weight
        self.cpu_cores = cpu_cores
        self.harddrive_size = harddrive_size
        self.battery_info = battery_info
        self.os_name = os_name
        self.touchscreen = touchscreen
        self.camera = camera
        self.brand = brand
        self.price = price
        self.model = model

 