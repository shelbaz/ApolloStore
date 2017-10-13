
from project.models.item_model import Item
from project.models import connect_to_db


class TabletGateway(Item):

    # Adds the tablet to the database
    @staticmethod
    def insert_into_db(tablet):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO tablets (model, display_size, dimensions, processor, ram_size, cpu_cores, hd_size, battery, os, camera_info) VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s', '%s');"""
                    % (tablet.model, tablet.display_size, tablet.dimensions, tablet.processor, str(tablet.ram_size), str(tablet.cpu_cores), str(tablet.hd_size), tablet.battery, tablet.os, tablet.camera_info))
