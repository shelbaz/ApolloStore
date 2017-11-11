# -----------------------------------------------------------------
# This stores all the possible configurations for the flask app.
#
# For variable configurations like the secret key or the database
# url, they should be stored as environment variables and imported
# using the 'os' library in Python.
# -----------------------------------------------------------------


import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    RESULT_BACKEND = os.getenv('CELERY_BROKER_URL')
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
