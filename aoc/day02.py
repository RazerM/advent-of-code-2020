from abc import ABC, abstractmethod
from collections import Counter

import attr
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

from .registry import register


grammar = r'''
    lines = line (nl line)* nl? EOF
    line = policy ":" ws password
    password = letter+
    policy = uint "-" uint ws letter
    letter = r'[a-z]'
    uint = digit+
    digit = r'[0-9]'
    ws = r'[ \t]+'
    nl = r'[\r\n]+'
'''


@attr.s
class Policy(ABC):
    num1 = attr.ib()
    num2 = attr.ib()
    letter = attr.ib()

    @abstractmethod
    def check(self, password):
        raise NotImplementedError


class FrequencyPolicy(Policy):
    def check(self, password):
        c = Counter(password)
        allowed = range(self.num1, self.num2 + 1)
        return c[self.letter] in allowed


class PositionPolicy(Policy):
    def check(self, password):
        c1 = password[self.num1 - 1]
        c2 = password[self.num2 - 1]
        return bool(c1 == self.letter) ^ bool(c2 == self.letter)


class PasswordVisitor(PTNodeVisitor):
    def __init__(self, *, policy_cls, **kwargs):
        self.policy_cls = policy_cls
        super().__init__(**kwargs)

    def visit_lines(self, node, children):
        return children

    def visit_line(self, node, children):
        return children

    def visit_password(self, node, children):
        return ''.join(children)

    def visit_policy(self, node, children):
        return self.policy_cls(num1=children[0], num2=children[1], letter=children[2])

    def visit_ws(self, node, children):
        pass

    def visit_nl(self, node, children):
        pass

    def visit_uint(self, node, children):
        return int(''.join(children))


def count_valid(parse_tree, policy_cls):
    return sum(
        policy.check(password)
        for policy, password
        in visit_parse_tree(parse_tree, PasswordVisitor(policy_cls=policy_cls))
    )


@register(day=2)
def solve(file, verbose):
    parser = ParserPEG(grammar, root_rule_name='lines', skipws=False)
    parse_tree = parser.parse(file.read())
    print('Part 1:', count_valid(parse_tree, policy_cls=FrequencyPolicy))
    print('Part 2:', count_valid(parse_tree, policy_cls=PositionPolicy))


