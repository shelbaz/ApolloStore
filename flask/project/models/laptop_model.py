
from project.models.item_model import Item
from project.models import connect_to_db
import psycopg2


class Laptop(Item):

    # Constructor that creates a new laptop
    def __init__(self, model, brand, price, weight, display_size, processor, ram_size, cpu_cores, hd_size, battery_info, os, touchscreen, camera):

        # Creates the Item object
        super().__init__(model, brand, price, weight)

        # Initialize object attributes
        self.model = model
        self.display_size = display_size
        self.processor = processor
        self.ram_size = ram_size
        self.cpu_cores = cpu_cores
        self.hd_size = hd_size
        self.battery_info = battery_info
        self.os = os
        self.touchscreen = touchscreen
        self.camera = camera
