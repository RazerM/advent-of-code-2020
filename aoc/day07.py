from typing import List, Optional

import attr
import networkx as nx
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

from .registry import register

grammar = r'''
    rules = rule+ EOF
    rule = bag "contain" bags_or_empty "."
    bags_or_empty = bags / empty
    bags = quantity_bag ("," quantity_bag)*
    empty = "no other bags"
    quantity_bag = uint bag
    bag = word word bag_kw
    bag_kw = "bags" / "bag"
    word = r'\w+'
    uint = r'[0-9]+'
'''


@attr.s(auto_attribs=True)
class Bag:
    name: str
    quantity: Optional[int] = None


@attr.s(auto_attribs=True)
class Rule:
    bag: Bag
    contains: List[Bag]


class BagVisitor(PTNodeVisitor):
    def visit_rules(self, node, children):
        return children

    def visit_rule(self, node, children):
        return Rule(children[0], children[1])

    def visit_bags(self, node, children):
        return children

    def visit_empty(self, node, children):
        return []

    def visit_quantity_bag(self, node, children):
        quantity, bag = children
        bag.quantity = quantity
        return bag

    def visit_bag(self, node, children):
        return Bag(' '.join(children))

    def visit_bag_kw(self, node, children):
        return

    def visit_uint(self, node, children):
        return int(str(node))


def count_bags(graph, node):
    total = 0
    for n, data in graph[node].items():
        total += data['quantity'] * (1 + count_bags(graph, n))
    return total


@register(day=7)
def solve(file, verbose):
    parser = ParserPEG(grammar, root_rule_name='rules')
    parse_tree = parser.parse(file.read())
    rules = visit_parse_tree(parse_tree, BagVisitor())

    graph = nx.DiGraph()
    for rule in rules:
        for bag in rule.contains:
            graph.add_edge(rule.bag.name, bag.name, quantity=bag.quantity)

    print('Part 1:', len(nx.ancestors(graph, 'shiny gold')))
    print('Part 2:', count_bags(graph, 'shiny gold'))
