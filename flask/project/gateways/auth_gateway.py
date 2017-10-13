
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

    # Queries the users table with the filters given as parameters (only equality filters)
    @staticmethod
    def query_filtered_by(**kwargs):
        """
        Example usage: User.query_filtered_by(first_name='Elon', last_name='Bean')
        will return a list of User object with the conditions given as parameters
        """

        filters = []

        for key, value in kwargs.items():
            filters.append(str(key) + '=\'' + str(value) + '\'')

        filters = ' AND '.join(filters)

        if filters:
            query = """SELECT * FROM users WHERE %s;""" % (filters,)
        else:
            query = """SELECT * FROM users;"""

        with connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
