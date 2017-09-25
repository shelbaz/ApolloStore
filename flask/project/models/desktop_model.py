
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Desktop(Item):

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
                          model UUID PRIMARY KEY,
                          processor varchar(64),
                          ram_size integer,
                          cpu_cores integer,
                          hd_size integer,
                          dimensions varchar(64),
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Constructor that creates a new desktop
    def __init__(self, model, price, weight, brand, processor, ram_size, cpu_cores, hd_size, dimensions):

        # Creates the Item object
        super().__init__(model, price, weight, brand)

        # Initialize object attributes
        self.model = model
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.dimensions = dimensions

    # Adds the desktop to the database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                super().insert_into_db()
                cursor.execute(
                    """INSERT INTO desktops (model, processor, ram_size, cpu_cores, hd_size, dimensions) VALUES ('%s', '%s', %s, %s, %s, '%s');"""
                    % (self.model, self.processor, str(self.ram_size), str(self.cpu_cores), str(self.hd_size), self.dimensions))

    # Queries the desktops table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        query = """SELECT * FROM desktops WHERE %s;""" % (filters,)

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        desktops = []

        for row in rows:
            desktops = Desktop(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            desktops.append(desktops)

        if desktops:
            return desktops
        else:
            return None
