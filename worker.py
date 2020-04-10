import os

import redis
from rq import Worker, Queue, Connection

from decouple import config

import logging

worker_logger = logging.getLogger(__name__)

listen = ['default']

redis_url = config('REDISTOGO_URL', default='redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker_logger.info('Starting redis worker listening.')
        worker = Worker(list(map(Queue, listen)))
        worker.work()
