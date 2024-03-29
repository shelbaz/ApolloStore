
from passlib.apps import custom_app_context as pwd_context
from project.orm import Mapper


class User(Mapper):

    name = 'users'

    attributes = {
        'id': 'UUID',
        'first_name': 'varchar(64)',
        'last_name': 'varchar(64)',
        'address': 'varchar(256)',
        'email': 'varchar(128)',
        'password_hash': 'varchar(256)',
        'phone': 'varchar(64)',
        'admin': 'boolean',
        'logged_in': 'boolean',
        'time_stamp': 'timestamp'
    }

    constraints = {
        'PRIMARY KEY': '(id)',
        'UNIQUE': '(email)'
    }

    # Constructor that creates a new user
    def __init__(self, id, first_name, last_name, address, email, phone, admin, logged_in, time_stamp):

        super().__init__(__class__.name, __class__.attributes, __class__.constraints)

        # Initializes object attributes
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.phone = phone
        self.admin = admin
        self.logged_in = logged_in
        self.time_stamp = time_stamp

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
