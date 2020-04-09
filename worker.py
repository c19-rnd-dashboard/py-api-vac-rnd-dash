import os

import redis
from rq import Worker, Queue, Connection

from decouple import config

listen = ['default']

redis_url = config('REDISTOGO_URL', default='redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
