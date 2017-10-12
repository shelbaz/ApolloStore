
from project.models import connect_to_db
import psycopg2


class Inventory(object):

    # Constructor that creates inventory
    def __init__(self, id, model):

        # Initialize object attributes
        self.id = id
        self.model = model

