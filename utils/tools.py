import functools


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
