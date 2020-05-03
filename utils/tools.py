import functools
import time


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
    for i in range(max_tries):
        try:
            fun()
            break
        except Exception as e:
            time.sleep(time_between_retries)
            logger("Retry #{retry_count},Max Tries: {max_tries},Time in between retries: {time_between_retries}, Exception: {e}").format(
                {'retry_count': i, 'e': e, 'time_between_retries': time_between_retries, 'max_tries': max_tries})
            continue


def assign_prop(prop_name, value, obj):
    obj[prop_name] = value
    return obj


def flatten(l): return [item for sublist in l for item in sublist]
