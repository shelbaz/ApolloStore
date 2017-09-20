
import psycopg2
import time


# Creates a connection to the PostgreSQL
def connect_to_db():
    with psycopg2.connect('postgresql://postgres:postgres@postgres:5432/db_dev') as connection:
        return connection


# Calls the class functions that create the tables of the corresponding models
def create_tables():
    try:
        from project.models.auth_model import User
        User.create_table()
    except Exception:
        # Safeguards against the first time creating the Docker volume, where postgres/create.sql didn't finish running
        time.sleep(5)
        create_tables()
