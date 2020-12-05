from itertools import combinations
import math

from .registry import register


def find_2020_sum(entries, n):
    if not isinstance(entries, set):
        entries = set(entries)
    for tuples in combinations(entries, n - 1):
        target = 2020 - sum(tuples)
        if target in entries:
            return math.prod(tuples) * target


@register(day=1)
def solve(file, verbose):
    entries = {int(entry) for entry in file}
    print('Part 1:', find_2020_sum(entries, 2))
    print('Part 2:', find_2020_sum(entries, 3))
