from typing import List, Set

from .registry import register


@register(day=6)
def solve(file, verbose):
    groups: List[List[Set]] = []
    group: List[Set] = []

    for line in file:
        line = line.strip()
        if line:
            group.append(set(line))
        else:
            groups.append(group)
            group = []
    groups.append(group)

    print('Part 1:', sum(len(set.union(*group)) for group in groups))
    print('Part 2:', sum(len(set.intersection(*group)) for group in groups))
