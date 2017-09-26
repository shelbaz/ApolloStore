
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from project import logger
from project.models.auth_model import User
from re import match
from uuid import uuid4
import traceback

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')


# Creates a user that is valid
def create_user(first_name, last_name, address, email, password, phone, admin):
    try:
        if validate_email(email):
            if validate_name(first_name) and validate_name(last_name):
                if validate_password(password):
                    if User.query_filtered_by(email=email) is None:

                        user = User(id=str(uuid4()), first_name=first_name, last_name=last_name, address=address, email=email, phone=phone, admin=admin)
                        user.hash_password(password)
                        user.insert_into_db()

                        logger.info('User with email %s successfully created' % (email,))

                        return user

    except Exception as e:
        logger.error(traceback.format_exc())


def validate_email(email):
    regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if match(regex, email) is not None:
        return True
    else:
        return False


def validate_name(name):
    regex = '^[A-Za-z-]{1,64}$'
    if match(regex, name) is not None:
        return True
    else:
        return False


def validate_password(password):
    regex = '^(?=.*\d).{8,20}$'
    if match(regex, password) is not None:
        return True
    else:
        return False


# Verifies email and password credentials
@basic_auth.verify_password
def verify_password(email, password):
    user = User.query_filtered_by(email=email)
    if not user or not user[0].verify_password(password):
        return False
    g.user = user[0]
    return True


# Verifies authentication token credentials
@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True
