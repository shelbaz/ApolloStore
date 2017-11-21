# ------------------------------------------------------------------
# This is the root of the main package of the Flask app: project.
#
# Whenever you see 'from project import [something]', it takes it
# from here.
# ------------------------------------------------------------------

from flask import Flask
import os
import logging
from celery import Celery
from flask_login import LoginManager

# Defines the format of the logging to include the time and to use the INFO logging level or worse.
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

login_manager = LoginManager()

from project.identityMap import IdentityMap
identity_map = IdentityMap()

celery = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL'))

# Defines the application factory. Every time this function is called, a new application
# instance is created. The reason why an application factory is needed is because we
# need to use different configurations for running our tests.
def create_app():
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')

    try:
        app.config.from_object(app_settings)
    except ImportError:
        import sys
        sys.path.append('/usr/src/app')
        app.config.from_object(app_settings)

    login_manager.init_app(app)

    celery.conf.update(app.config)

    # Imports the 'website_blueprint' to apply it to the application instance.
    # In order to define routes/endpoints in Flask, you need to write something
    # like @app.route('/endpoint1'). Since we don't initialize our application
    # variable here, but use an application factory instead, we can't import 'app'.
    #
    # Instead, blueprints are used. If you want to read more about it, visit:
    # http://flask.pocoo.org/docs/0.12/blueprints/
    from project.website.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from project.website.views import website_blueprint
    app.register_blueprint(website_blueprint)

    return app
