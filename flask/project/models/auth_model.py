
import psycopg2


class User():

    @staticmethod
    def create_table():
        connect = psycopg2.connect('postgresql://postgres:postgres@postgres:5432/db_dev')
        cursor = connect.cursor()
        cursor.execute(
            """
            CREATE TABLE users(
              id UUID PRIMARY KEY,
              first_name varchar(64),
              last_name varchar(64),
              address varchar(256),
              email varchar(128),
              phone varchar(64),
              admin boolean      
            );
            """
        )
        connect.commit()
        connect.close()

    def __init__(self, first_name, last_name, address, email, phone, account_type):
        pass

