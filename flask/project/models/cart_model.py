
from project.models import connect_to_db
import psycopg2


class Cart(object):

    # Constructor that creates a new cart
    def __init__(self, id, inventory_id, user_id, added_time):

        # Initialize the object's attributes
        self.id = id
        self.inventory_id = inventory_id
        self.user_id = user_id
        self.added_time = added_time

