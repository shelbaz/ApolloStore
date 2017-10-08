
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Tablet(Item):

    # Constructor that creates a new tablet
    def __init__(self, model, brand, price, weight, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.display_size = display_size
        self.dimensions = dimensions
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.battery = battery
        self.os = os
        self.camera_info = camera_info

 