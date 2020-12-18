from collections import Counter

from .registry import register


def find_candidates(adapters, joltage):
    return adapters.intersection(joltage + i for i in range(1, 4))


def part1(adapters):
    builtin_adapter = max(adapters) + 3
    adapters.add(builtin_adapter)

    current_joltage = 0

    differences = []
    counter = Counter()

    while candidates := find_candidates(adapters, current_joltage):
        next_joltage = min(candidates)
        adapters.remove(next_joltage)
        differences.append(next_joltage - current_joltage)
        counter[next_joltage - current_joltage] += 1
        current_joltage = next_joltage

    return counter[1] * counter[3]


@register(day=10)
def solve(file, verbose):
    adapters = {int(line.strip()) for line in file}

    print('Part 1:', part1(adapters))
