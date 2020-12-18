import math
from typing import Tuple

from .registry import register


def extended_euclidean(a, b) -> Tuple[int, int]:
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_s, old_t


def chinese_remainder_theorem(moduli, remainders):
    n1 = moduli[0]
    a1 = remainders[0]

    for n2, a2 in zip(moduli[1:], remainders[1:]):
        m1, m2 = extended_euclidean(n1, n2)
        a1 = a1 * m2 * n2 + a2 * m1 * n1
        n1 = n1 * n2

    return a1 % math.prod(moduli)


@register(day=13)
def solve(file, verbose):
    it = iter(file)
    earliest_departure = int(next(it))
    buses = [
        (id_ := int(v), id_ - i)
        for i, v in enumerate(next(it).rstrip().split(','))
        if v != 'x'
    ]
    wait, id_ = min((id_ - earliest_departure % id_, id_) for id_, _ in buses)
    print('Part 1:', wait * id_)
    print('Part 2:', chinese_remainder_theorem(*zip(*buses)))
