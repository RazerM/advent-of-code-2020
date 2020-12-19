import math
import re
from typing import List, Optional

import attr

from .registry import register


@attr.s(auto_attribs=True)
class Field:
    name: str
    valid_ranges: List[range]
    pos: Optional[int] = None

    def check(self, value: int) -> bool:
        return any(value in range_ for range_ in self.valid_ranges)


def parse(file):
    rules = []
    get_my_ticket = False
    get_nearby_tickets = False
    my_ticket = None
    nearby_tickets = []

    for line in file:
        line = line.rstrip()

        if not line:
            continue

        if get_my_ticket:
            my_ticket = list(map(int, line.split(',')))
            get_my_ticket = False

        elif get_nearby_tickets:
            nearby_tickets.append(list(map(int, line.split(','))))

        elif match := re.match(r'^([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)', line):
            field, l1, u1, l2, u2 = match.groups()
            l1, u1, l2, u2 = map(int, [l1, u1, l2, u2])
            rules.append(Field(field, [range(l1, u1 + 1), range(l2, u2 + 1)]))

        elif line == 'your ticket:':
            get_my_ticket = True

        elif line == 'nearby tickets:':
            get_nearby_tickets = True

    return rules, my_ticket, nearby_tickets


def find_valid_tickets(rules, nearby_tickets):
    error_rate = 0

    valid_tickets = []

    for ticket in nearby_tickets:
        valid = True
        for value in ticket:
            if not any(rule.check(value) for rule in rules):
                error_rate += value
                valid = False
        if valid:
            valid_tickets.append(ticket)

    return valid_tickets, error_rate


def determine_fields(rules, valid_tickets):
    num_fields = len(valid_tickets[0])
    found = set()

    while any(rule.pos is None for rule in rules):
        for i in range(num_fields):
            if i in found:
                continue
            col = [ticket[i] for ticket in valid_tickets]

            matching_rules = (
                rule for rule in rules
                if rule.pos is None and all(rule.check(value) for value in col)
            )

            try:
                rule, = matching_rules
            except ValueError:
                continue
            else:
                found.add(i)
                rule.pos = i


@register(day=16)
def solve(file, verbose):
    rules, my_ticket, nearby_tickets = parse(file)

    valid_tickets, error_rate = find_valid_tickets(rules, nearby_tickets)
    print('Part 1:', error_rate)

    determine_fields(rules, valid_tickets)
    print('Part 2:', math.prod(
        my_ticket[rule.pos] for rule in rules if rule.name.startswith('departure')
    ))
