from collections.abc import Iterator
from itertools import islice


def minmax(iterable):
    if isinstance(iterable, Iterator):
        iterable = list(iterable)
    return min(iterable), max(iterable)


def take(n, iterable):
    return list(islice(iterable, n))
