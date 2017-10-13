
from project.models.item_model import Item
from project.models import connect_to_db


class DesktopGateway(Item):

    # Adds the desktop to the database
    @staticmethod
    def insert_into_db(desktop):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO desktops (model, processor, ram_size, cpu_cores, hd_size, dimensions) VALUES ('%s', '%s', %s, %s, %s, '%s');"""
                    % (desktop.model, desktop.processor, str(desktop.ram_size), str(desktop.cpu_cores), str(desktop.hd_size), desktop.dimensions))
