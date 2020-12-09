from collections.abc import Iterator


def minmax(iterable):
    if isinstance(iterable, Iterator):
        iterable = list(iterable)
    return min(iterable), max(iterable)
