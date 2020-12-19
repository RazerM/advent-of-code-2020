from functools import lru_cache

import regex
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

from .registry import register


@lru_cache(maxsize=None)
def get_rule_parser():
    grammar = '''
        rule = int ':' (str / seq ('|' seq)*)
        seq = int+
        str = '"' r'[^"]+' '"'
        int = r'[0-9]+'
    '''
    return ParserPEG(grammar, root_rule_name='rule')


class RuleVisitor(PTNodeVisitor):
    def visit_rule(self, node, children):
        idx, *values = children
        if len(values) == 1 and isinstance(values[0], str):
            return idx, values[0]
        else:
            return idx, values

    def visit_seq(self, node, children):
        return children

    def visit_str(self, node, children):
        return children[0]

    def visit_int(self, node, children):
        return int(node.value)


def parse_rule(s):
    rule_parser = get_rule_parser()
    parse_tree = rule_parser.parse(s)
    return visit_parse_tree(parse_tree, RuleVisitor())


def count_matches(rules, messages):
    definitions = ''
    for idx, contents in rules.items():
        if isinstance(contents, str):
            pattern = contents
        else:
            pattern = '|'.join(
                ''.join(f'(?&r{i})' for i in variant) for variant in contents
            )
        definitions += f'(?P<r{idx}>{pattern})'

    pattern = regex.compile(f'(?(DEFINE){definitions})^(?&r0)$')
    return sum(bool(pattern.match(m)) for m in messages)


@register(day=19)
def solve(file, verbose):
    rules = dict()

    for line in file:
        line = line.rstrip()

        if not line:
            break

        idx, contents = parse_rule(line)
        rules[idx] = contents

    messages = [line.rstrip() for line in file]

    print('Part 1:', count_matches(rules, messages))
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    print('Part 2:', count_matches(rules, messages))
