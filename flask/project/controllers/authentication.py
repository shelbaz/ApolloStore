
from project import logger, login_manager
from project.models.auth import User
from re import match
from uuid import uuid4
import traceback
from project.orm import Mapper


class AuthenticationController():

    # Creates a user that is valid
    @staticmethod
    def create_user(first_name, last_name, address, email, password, phone, admin):
        try:
            if AuthenticationController.validate_email(email):
                if AuthenticationController.validate_name(first_name) and AuthenticationController.validate_name(last_name):
                    # if validate_password(password):
                    if not Mapper.query('users', email=email):
                        user = User(id=str(uuid4()), first_name=first_name, last_name=last_name, address=address, email=email, phone=phone, admin=admin)
                        user.hash_password(password)
                        user.insert()

                        logger.info('User with email %s successfully created' % (email,))

                        return user

        except Exception:
            logger.error(traceback.format_exc())

    @staticmethod
    def validate_email(email):
        regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        if match(regex, email) is not None:
            return True
        else:
            return False

    @staticmethod
    def validate_name(name):
        regex = '^[A-Za-z-]{1,64}$'
        if match(regex, name) is not None:
            return True
        else:
            return False

    @staticmethod
    def validate_password(password):
        regex = '^(?=.*\d).{8,20}$'
        if match(regex, password) is not None:
            return True
        else:
            return False

    @staticmethod
    def get_user_from_rows(rows):
        if rows:
            users = []
            for row in rows:
                user = User(row[0], row[1], row[2], row[3], row[4], row[6], row[7])
                user.password_hash = row[5]
                users.append(user)

            if users:
                return users[0]
            else:
                return None
        else:
            return None

    @login_manager.user_loader
    def load_user(user_id):

        rows = []
        rows = Mapper.query('users', id=user_id)
        users = []

        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4], row[6], row[7])
            user.password_hash = row[5]
            users.append(user)

        if users:
            return users[0]
        else:
            return None