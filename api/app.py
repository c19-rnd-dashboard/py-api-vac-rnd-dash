"""Main application and routing logic for Vaccine R&D Dash API."""
from flask import Flask, json, jsonify, request
from api.routes.mock_routes import mock_routes
from flask_cors import CORS
from flask_caching import Cache
from decouple import config
import os

# Logging
import logging

###########
###Setup###
###########
# Local Environment Testing Only.
#   Un-comment to build environment script in config.py
# from instance import setup
# setup.setup_env()


# Set database name
local_db_name = 'test.sqlite3'  # Change this or override with config.py file in instance/

def create_app(test_config=None):
    """
    Creates app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DEBUG=config('DEBUG', default=False),  # Make sure to change debug to False in production env
        SECRET_KEY=config('SECRET_KEY', default='dev'),  # CHANGE THIS!!!!
        DATABASE_URI=config('DATABASE_URI', 'sqlite:///' + os.path.join(os.getcwd(), local_db_name)),  # For in-memory db: default='sqlite:///:memory:'),
        LOGFILE=config('LOGFILE', os.path.join(app.instance_path, 'logs/debug.log')),
        CACHE_TYPE=config('CACHE_TYPE', 'simple'),  # Configure caching
        CACHE_DEFAULT_TIMEOUT=config('CACHE_DEFAULT_TIMEOUT', 300), # Long cache times probably ok for ML api
    )

    # Enable CORS header support
    CORS(app)

    # Enable caching
    cache = Cache(app)

    ##############
    ### Routes ###
    ##############
    app.register_blueprint(mock_routes)

    #############
    ###Logging###
    #############
    # Change logging.INFO to logging.DEBUG to get full logs.  Will be a crapload of information.
    # May significantly impair performance if writing logfile to disk (or network drive).
    # To enable different services, see README.md
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    logging.basicConfig(filename=app.config['LOGFILE'], level=logging.INFO)  # File logging. Remove in PROD
    logging.getLogger('flask_cors').level = logging.INFO
    app_logger = logging.getLogger(__name__)

    # Register database functions.  Will allow db.close() to run on teardown
    from api import db
    db.init_app(app)

    return app
