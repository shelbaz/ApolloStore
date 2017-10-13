
from project.models import connect_to_db


class CartGateway(object):

    # Insert cart into database
    def insert_into_db(self):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO carts (id, inventory_id, user_id, added_time) VALUES ('%s', '%s', '%s', '%s');"""
                    % (self.id, self.inventory_id, self.user_id, self.added_time))
