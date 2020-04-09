"""
Messenger Queue
    Initialize messenger queue and allow global fetch of queue object.
"""

from rq import Queue
from rq.job import Job
from worker import conn

from flask import current_app, g
from flask.cli import with_appcontext

import logging
mq_logger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


def get_q():
    """
    Returns current messenger queue.  If connection not present, initiates connection to 
    to configured messenger.
    """
    if 'q' not in g:
        mq_logger.info('Redis connection not found. Attempting connection to {}.'.format(current_app.config['REDISTOGO_URL']))
        try:
            q = Queue(connection=conn)
            g.q = q
        except:
            mq_logger.error('Could not establish connection.  Aborting.')
            raise ConnectionError

    return g.q