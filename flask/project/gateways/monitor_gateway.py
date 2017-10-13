
from project.models.item_model import Item
from project.models import connect_to_db


class MonitorGateway(Item):

    # Adds the monitor to the database
    @staticmethod
    def insert_into_db(monitor):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO monitors (model, dimensions) VALUES ('%s', '%s');"""
                    % (monitor.model, monitor.dimensions))
