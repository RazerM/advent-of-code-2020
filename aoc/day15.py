import array
from itertools import count, repeat

from .itertools import nth
from .registry import register


def speak_numbers(numbers):
    last_spoken_when = array.array('I', repeat(0, 10000))

    for i, n in enumerate(numbers, start=1):
        yield n
        last_spoken_when[n] = i

    spoken = numbers[-1]

    for i in count(len(numbers)):
        try:
            when = last_spoken_when[spoken]
        except IndexError:
            # double length of array
            last_spoken_when.extend(repeat(0, len(last_spoken_when)))
            next_spoken = 0
        else:
            next_spoken = 0 if when == 0 else i - when
        last_spoken_when[spoken] = i
        yield spoken
        spoken = next_spoken


@register(day=15)
def solve(file, verbose):
    numbers = [int(x) for x in file.read().split(',')]

    print('Part 1:', nth(speak_numbers(numbers), 2020))
    print('Part 2:', nth(speak_numbers(numbers), 30_000_000))
