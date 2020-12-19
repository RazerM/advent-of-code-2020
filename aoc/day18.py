import math

from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

from .registry import register

simple_grammar = '''
    expr = factor (op factor)*
    factor = int / '(' expr ')'
    op = '*' / '+'
    int = r'[0-9]+'
'''

advanced_grammar = '''
    expr = term ('*' term)*
    term = factor ('+' factor)*
    factor = int / '(' expr ')'
    int = r'[0-9]+'
'''


class SimpleVisitor(PTNodeVisitor):
    def visit_expr(self, node, children):
        expr = 0
        for i in range(0, len(children), 2):
            if i and children[i - 1] == '*':
                expr *= children[i]
            else:
                expr += children[i]

        return expr

    def visit_factor(self, node, children):
        return children[0]

    def visit_int(self, node, children):
        return int(node.value)


class AdvancedVisitor(PTNodeVisitor):
    def visit_expr(self, node, children):
        return math.prod(children)

    def visit_term(self, node, children):
        return sum(children)

    def visit_factor(self, node, children):
        return children[0]

    def visit_int(self, node, children):
        return int(node.value)


@register(day=18)
def solve(file, verbose):
    simple_parser = ParserPEG(simple_grammar, root_rule_name='expr')
    advanced_parser = ParserPEG(advanced_grammar, root_rule_name='expr')
    simple_sum = 0
    advanced_sum = 0

    for line in file:
        parse_tree = simple_parser.parse(line)
        simple_sum += visit_parse_tree(parse_tree, SimpleVisitor())
        parse_tree = advanced_parser.parse(line)
        advanced_sum += visit_parse_tree(parse_tree, AdvancedVisitor())

    print('Part 1:', simple_sum)
    print('Part 2:', advanced_sum)
