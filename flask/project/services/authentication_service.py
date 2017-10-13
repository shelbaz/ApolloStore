from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from project import logger, login_manager
from project.models.auth_model import User
from project.gateways.auth_gateway import UserGateway
from re import match
from uuid import uuid4
import traceback


class AuthenticationService():
    # Creates a user that is valid

    @staticmethod
    def create_user(first_name, last_name, address, email, password, phone, admin):
        try:
            if AuthenticationService.validate_email(email):
                if AuthenticationService.validate_name(first_name) and AuthenticationService.validate_name(last_name):
                    # if validate_password(password):
                    if UserGateway.query_filtered_by(email=email) is None:
                        user = User(id=str(uuid4()), first_name=first_name, last_name=last_name, address=address, email=email, phone=phone, admin=admin)
                        user.hash_password(password)
                        UserGateway.insert_into_db(user)

                        logger.info('User with email %s successfully created' % (email,))

                        return user

        except Exception as e:
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
        rows = UserGateway.query_filtered_by(id=user_id)
        users = []

        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4], row[6], row[7])
            user.password_hash = row[5]
            users.append(user)

        if users:
            return users[0]
        else:
            return None
