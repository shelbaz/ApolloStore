
from project.models import connect_to_db


class UserGateway():

    # Adds the user to the database
    @staticmethod
    def insert_into_db(user):
        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (id, first_name, last_name, address, email, password_hash, phone, admin) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %s);"""
                    % (user.id, user.first_name, user.last_name, user.address, user.email, user.password_hash, user.phone, str(user.admin)))
