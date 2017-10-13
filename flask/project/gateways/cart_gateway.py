from project.models import connect_to_db
import psycopg2


class CartGateway(object):

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
                          inventory_id UUID UNIQUE,
                          user_id UUID,
                          added_time timestamp,
                          FOREIGN KEY (inventory_id) REFERENCES inventories (id),
                          FOREIGN KEY (user_id) REFERENCES users (id)
                        );
                        """
                    )

    # Class function that deletes the 'carts' table
    @staticmethod
    def drop_table():
        # Using the 'with' statement automatically commits and closes database connections
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                # Searches if there is already a table named 'carts'
                cursor.execute("select * from information_schema.tables where table_name=%s", ('carts',))

                # Deletes table 'carts' if it exists
                if bool(cursor.rowcount):
                    cursor.execute('DROP TABLE carts;')

    # Insert cart into database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO carts (id, inventory_id, user_id, added_time) VALUES ('%s', '%s', '%s', '%s');"""
                    % (self.id, self.inventory_id, self.user_id, self.added_time))

    @staticmethod
    # Queries the carts table with the filters given as parameters (only equality filters)
    def query_filtered_by(**kwargs):

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = 'SELECT * FROM carts WHERE %s;' % (filters,)
        else:
            query = 'SELECT * FROM carts;'

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None

        '''
        carts = []

        for row in rows:
            carts = Cart(row[0], row[1], row[2], row[3])
            carts.append(carts)

        if carts:
            return carts
        else:
            return None
        '''