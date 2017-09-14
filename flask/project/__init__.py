
from flask import Flask, g, request, current_app
import os
import logging


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    from project.website.views import website_blueprint
    app.register_blueprint(website_blueprint)

    return app
