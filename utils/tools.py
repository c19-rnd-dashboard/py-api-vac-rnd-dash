import functools
import time
import hashlib


def compose(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))
    return functools.reduce(compose2, functions, lambda x: x)


def find(f):
    """Return first item in sequence where f(item) == True."""
    def excecution(seq):
        for item in seq:
            if f(item):
                return item
    return excecution


def retry(fun, max_tries=10, time_between_retries=0.3, logger=print):
    def _retry(param):
        for i in range(max_tries):
            try:
                result = fun(param)
                if result != None:
                    return result
            except Exception as e:
                time.sleep(time_between_retries)
                logger("Retry #{},Max Tries: {},Time in between retries: {}, Exception: {}".format(
                    i, max_tries, time_between_retries, e))
                continue
    return _retry


def assign_prop(prop_name, value, obj):
    obj[prop_name] = value
    return obj


def flatten(l): return [item for sublist in l for item in sublist]


def generate_hash(input: str) -> str:
    return hashlib.sha1(input.encode('utf-8')).hexdigest()
