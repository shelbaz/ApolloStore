
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Television(Item):

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
                        DO $$
                        BEGIN
                            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'types') THEN
                                CREATE TYPE types AS ENUM ('HD', 'LED', '3D', 'Smart');
                            END IF;
                        END$$;
                        CREATE TABLE televisions (
                          model UUID PRIMARY KEY,
                          type types,
                          dimensions varchar(64),
                          FOREIGN KEY (model) REFERENCES items (model)
                        );
                        """
                    )

    # Class function that deletes the 'televisions' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'televisions'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('televisions',))

                # Deletes table 'televisions' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE televisions;')

    # Constructor that creates a new television
    def __init__(self, model, price, weight, brand, type, dimensions):

        # Creates the Item object
        super().__init__(model, price, weight, brand)

        # Initialize object attributes
        self.model = model
        self.type = type
        self.dimensions = dimensions

    # Adds the television to the database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                super().insert_into_db()
                cursor.execute(
                    """INSERT INTO televisions (model, type, dimensions) VALUES ('%s', '%s', '%s');"""
                    % (self.model, self.type, self.dimensions))

# Queries the televisions table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM televisions WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM televisions;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        televisions = []

        for row in rows:
            televisions = Television(row[0], row[1], row[2], row[3], row[4], row[5])
            televisions.append(televisions)

        if televisions:
            return televisions
        else:
            return None