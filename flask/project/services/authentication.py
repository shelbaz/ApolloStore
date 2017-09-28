
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from project import logger, login_manager
from project.models.auth_model import User
from re import match
from uuid import uuid4
import traceback


# Creates a user that is valid
def create_user(first_name, last_name, address, email, password, phone, admin):
    try:
        if validate_email(email):
            if validate_name(first_name) and validate_name(last_name):
                # if validate_password(password):
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


<<<<<<< HEAD
# Verifies credentials
@auth.verify_password
def verify_password(email_or_token, password):
    user = User.verify_auth_token(email_or_token)
    if not user:
        user = User.query_filtered_by(email=email_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user[0]
    return True
=======
@login_manager.user_loader
def load_user(user_id):
    user = User.query_filtered_by(id=user_id)
    if user:
        return user[0]
    else:
        return None
>>>>>>> dev
