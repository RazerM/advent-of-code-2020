from itertools import combinations

from .itertools import minmax
from .registry import register


def find_invalid(numbers, preamble):
    for i, n in enumerate(numbers[preamble:], start=preamble):
        if n not in (sum(x) for x in combinations(numbers[i - preamble:i], 2)):
            return n


def find_weakness(numbers, invalid_number):
    start = end = total = 0

    while total != invalid_number or end - start < 2:
        while total < invalid_number:
            total += numbers[end]
            end += 1
        while total > invalid_number:
            total -= numbers[start]
            start += 1

    return sum(minmax(numbers[start:end]))


@register(day=9)
def solve(file, verbose):
    numbers = [int(line) for line in file]
    invalid_number = find_invalid(numbers, 25)
    print('Part 1:', invalid_number)
    print('Part 2:', find_weakness(numbers, invalid_number))

