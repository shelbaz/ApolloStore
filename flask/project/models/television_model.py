
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Television(Item):

    # Constructor that creates a new television
    def __init__(self, model, brand, price, weight, type, dimensions):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.type = type
        self.dimensions = dimensions
