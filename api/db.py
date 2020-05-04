"""
Database
    Initialize and create connection control flow for database.
    Datase parameters must be set in config.py or directly in app.py
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import sys
from decouple import config
from contextlib import contextmanager
from api.models import *

import click
from flask import current_app, g
from flask.cli import with_appcontext

import logging

db_logger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

def get_db(context=True):
    """
    Returns current database connection.  If connection not present,
    initiates connection to configured database.  Default is non-authenticated SQL.
    Modifty g.db = *connect to match intended database connection.
    """

    if context == True:
        if 'db' not in g:
            db_logger.info('DB connection not found. Attempting connection to {}.'.format(config('DATABASE_URI')))
            try:
                g.engine = create_engine(current_app.config['DATABASE_URI'])
                g.db = g.engine.connect()
            except:
                db_logger.error('Could not establish connection.  Aborting.')
                raise ConnectionError
        return g.db

    else:
        db_logger.info("Creating new database connection without app context.")
        db_logger.info('DB connection not found. Attempting connection to {}.'.format(config('DATABASE_URI')))
        engine = create_engine(config('DATABASE_URI'))
        return engine.connect()


@contextmanager
def get_session(context=True):
    # Setup session with thread engine.
    #   Allows for usage: with get_session() as session: session...
    engine = get_db(context)
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session
    finally:
        session.close()
        close_db()  # May fix issues with connections to database remaining open, but not force connection closure until session activity completes


def close_db(e=None):
    db = g.pop('db', None)
    engine = g.pop('engine', None)
    if db is not None:
        db.close()
        engine.dispose()


def init_db(out=sys.stdout, context=True):
    db = get_db(context)
    Base.metadata.create_all(db)
    out.write('init called')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create tables from models.py"""
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
