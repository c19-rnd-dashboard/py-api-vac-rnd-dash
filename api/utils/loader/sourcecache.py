# sourcecache.py


from api.models import SourceCache
from api.db import get_session
from api.utils.transform import drop_unnamed_columns

import datetime
import pickle

import logging


cachelogger = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


cache_time = datetime.timedelta(days=1)


def _check_filename(obj):
    if hasattr(obj, 'filename'):
        return obj.filename
    return False


def _recent_cache(filename):
    
    def _get_age(uri):
        with get_session(context=False) as session:
            lupd = session.query(SourceCache.last_update).filter(SourceCache.uri == uri).all()
            try:
                if lupd[0]:
                    cachelogger.info(f'LastUpdate found at: {lupd[0][0]}')
                    age = datetime.datetime.now() - lupd[0][0]
                    return age
                return False
            except Exception as e:
                cachelogger.warn(f'Could not find cached instance: {e}')
                return False
                
    uri = filename
    
    age = _get_age(uri)
    if age:
        cachelogger.info(f'Cache found. Age: {age}')
        cachelogger.info(f'Testing age against threshold {cache_time}')
        cachelogger.info(f'Is {age} < {cache_time}: {age < cache_time}')
        return age < cache_time


def check_cache(*args, **kwargs):
    loader = args[0]
    if _check_filename(loader):
        cachelogger.info(f'Filename found in Loader.  Checking cache for recent load.')
        if _recent_cache(loader.filename):
            cachelogger.info(f'Valid cache identified.  Returning signal for cache read.')


def read_cache(*args, **kwargs):
    loader = args[0]

    def _unpickle(data):
        return pickle.loads(data)

    if _check_filename(loader):
        cachelogger.info(f'Filename found in Loader.  Checking cache for recent load.')
        if _recent_cache(loader.filename):
            cachelogger.info(f'Valid cache identified.  Loading data from cache.')
            with get_session(context=False) as session:
                result = session.query(SourceCache).filter(SourceCache.uri==loader.filename).all()
                return _unpickle(result[0].data)
    return False


def cache_source(*args, **kwargs):
    def _prep_data(data):
        temp = drop_unnamed_columns(data)
        return pickle.dumps(temp, pickle.HIGHEST_PROTOCOL)

    loader = args[0]
    name = loader.filename

    with get_session(context=False) as session:
        record = SourceCache(
            source_id=hash(name),
            uri=name,
            data=_prep_data(loader.fetch_transform()),
            last_update=datetime.datetime.now(),
            )
        session.add(record)
        session.commit()


def clear_cache(*args, **kwargs):
    with get_session(context=False) as session:
        try:
            num_rows_deleted = session.query(SourceCache).delete()
            session.commit()
            cachelogger.info(f'Deleted all cached sources.')
            return True
        except Exception as e:
            session.rollback()
            cachelogger.error(f'Could not delete cached sources. Error: {e}')
            return False