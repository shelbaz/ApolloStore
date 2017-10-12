
from project.models import connect_to_db
import psycopg2
import os
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User():

    # Constructor that creates a new user
    def __init__(self, id, first_name, last_name, address, email, phone, admin):

        # Initializes object attributes
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.phone = phone
        self.admin = admin

    # Hashes the password and initializes the user's password_hash attribute
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Verifies that the given password matches the user's password
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
