"""Main application and routing logic for Vaccine R&D Dash API."""
from flask import Flask, json, jsonify, request
from api.routes.mock_routes import mock_routes
from api.routes.admin_routes import admin_routes
from api.routes.covid_dash import covid_dash
from flask_cors import CORS
from api.cache import cache
from decouple import config
import os

# Logging
import logging

###########
###Setup###
###########
# Local Environment Testing Only.
#   Un-comment to build environment script in config.py or run setup files
if os.path.isfile(os.path.join(os.getcwd(), 'instance/setup.py')):
    print('Instance setup.py found at: ', os.path.join(os.getcwd(), 'instance/setup.py'))
    from instance import setup
    setup.setup_env(testing=True, local_dev=True)


def create_app(test_config=None):
    """
    Creates app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Make sure to change debug to False in production env
        DEBUG=config('DEBUG', default=False),
        SECRET_KEY=config('SECRET_KEY', default='dev'),  # CHANGE THIS!!!!
        # For in-memory db: default='sqlite:///:memory:'),
        DATABASE_URI=config('DATABASE_URI'),
        LOGFILE=config('LOGFILE', os.path.join(
            app.instance_path, 'logs/debug.log')),
        CACHE_TYPE=config('CACHE_TYPE', 'simple'),  # Configure caching
        # Long cache times probably ok for ML api
        CACHE_DEFAULT_TIMEOUT=config('CACHE_DEFAULT_TIMEOUT', 300),
        TESTING=config('TESTING', default='TRUE'),
        REDISTOGO_URL=config('REDISTOGO_URL', default='redis://localhost:6379'),
    )

    # Enable CORS header support
    CORS(app)

    # Enable caching
    cache.init_app(app)

    ##############
    ### Routes ###
    ##############
    app.register_blueprint(mock_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(covid_dash)

    #############
    ###Logging###
    #############
    # Change logging.INFO to logging.DEBUG to get full logs.  Will be a crapload of information.
    # May significantly impair performance if writing logfile to disk (or network drive).
    # To enable different services, see README.md
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info('Application logging Set')

    # File logging. Remove in PROD
    if app.config['TESTING'] == 'TRUE':
        app.logger.info('Using TESTING log config.')
        logging.basicConfig(
            filename=app.config['LOGFILE'], 
            level=logging.INFO, 
            format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')
    
    logging.getLogger('flask_cors').level = logging.INFO

    # Register database functions.  Will allow db.close() to run on teardown
    from api import db
    db.init_app(app)
    app.logger.info('Database functionality initialized.  Click commands available.')

    return app
