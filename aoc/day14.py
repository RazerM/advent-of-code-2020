import re
from itertools import chain, product, zip_longest

import attr

from .registry import register


@attr.s(auto_attribs=True)
class SetMask:
    mask: str


@attr.s(auto_attribs=True)
class SetMem:
    addr: int
    value: int


def decodev1(instructions):
    mask = 'X' * 36
    mem = dict()

    for instruction in instructions:
        if isinstance(instruction, SetMem):
            value = f'{instruction.value:036b}'
            mem[instruction.addr] = int(
                ''.join(v if m == 'X' else m for v, m in zip(value, mask)), 2
            )
        elif isinstance(instruction, SetMask):
            mask = instruction.mask

    return sum(mem.values())


def float_addrs(addr, mask):
    addr = f'{addr:036b}'
    addr = ''.join(a if m == '0' else m for a, m in zip(addr, mask))
    parts = addr.split('X')
    floaters = product('01', repeat=len(parts) - 1)
    for floaty_bits in floaters:
        bits = chain.from_iterable(zip_longest(parts, floaty_bits, fillvalue=''))
        yield int(''.join(bits), 2)


def decodev2(instructions):
    mask = '0' * 36
    mem = dict()

    for instruction in instructions:
        if isinstance(instruction, SetMem):
            for addr in float_addrs(instruction.addr, mask):
                mem[addr] = instruction.value
        elif isinstance(instruction, SetMask):
            mask = instruction.mask

    return sum(mem.values())


@register(day=14)
def solve(file, verbose):
    instructions = []

    for line in file:
        if match := re.match(r'^mem\[(\d+)]\s*=\s*(\d+)', line):
            addr, value = map(int, match.groups())
            instructions.append(SetMem(addr, value))
        elif match := re.match(r'^mask\s*=\s*([01X]+)', line):
            instructions.append(SetMask(match.group(1)))

    print('Part 1:', decodev1(instructions))
    print('Part 2:', decodev2(instructions))
