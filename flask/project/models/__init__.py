
from project.models.auth_model import User


def create_tables():
    User.create_table()
