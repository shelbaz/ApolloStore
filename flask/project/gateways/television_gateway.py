
from project.models.item_model import Item
from project.models import connect_to_db


class TelevisionGateway(Item):

    # Adds the television to the database
    @staticmethod
    def insert_into_db(tv):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO televisions (model, type, dimensions) VALUES ('%s', '%s', '%s');"""
                    % (tv.model, tv.type, tv.dimensions))
