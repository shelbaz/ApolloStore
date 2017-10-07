
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Monitor(Item):

    # Constructor that creates a new monitor
    def __init__(self, model, brand, price, weight, dimensions):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.dimensions = dimensions

