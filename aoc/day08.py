from enum import Enum

import attr
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

from .registry import register

grammar = r'''
    instructions = instruction (nl instruction)* nl? EOF
    instruction = op ws int
    op = "acc" / "jmp" / "nop"
    int = r'[+-][0-9]+'
    ws = r'[ \t]+'
    nl = r'[\r\n]+'
'''


class Op(Enum):
    ACC = 'acc'
    JMP = 'jmp'
    NOP = 'nop'


@attr.s(auto_attribs=True)
class Instruction:
    op: str
    arg: int


class CodeVisitor(PTNodeVisitor):
    def visit_instructions(self, node, children):
        return children

    def visit_instruction(self, node, children):
        return Instruction(*children)

    def visit_op(self, node, childre):
        return Op(str(node))

    def visit_int(self, node, children):
        return int(str(node))

    def visit_ws(self, node, children):
        pass

    def visit_nl(self, node, children):
        pass


class InfiniteLoop(Exception):
    def __init__(self, *args, accumulator, **kwargs):
        self.accumulator = accumulator
        super().__init__(*args, **kwargs)


def run_bootcode(instructions):
    seen = set()
    accumulator = 0
    pos = 0

    while True:
        if pos in seen:
            raise InfiniteLoop(accumulator=accumulator)
        seen.add(pos)

        try:
            instruction = instructions[pos]
        except IndexError:
            return accumulator

        if instruction.op is Op.ACC:
            accumulator += instruction.arg
        elif instruction.op is Op.JMP:
            pos += instruction.arg - 1
        elif instruction.op is Op.NOP:
            pass

        pos += 1


def swap_jmp_nop(instruction):
    if instruction.op is not Op.JMP and instruction.op is not Op.NOP:
        raise ValueError
    return attr.evolve(
        instruction,
        op=Op.JMP if instruction.op is Op.NOP else Op.NOP,
    )


def make_variant(instructions, i):
    yield from instructions[:i]
    yield swap_jmp_nop(instructions[i])
    yield from instructions[i + 1:]


def variants(instructions):
    for i, instruction in enumerate(instructions):
        if instruction.op is Op.JMP or instruction.op is Op.NOP:
            yield make_variant(instructions, i)


def part1(instructions):
    try:
        run_bootcode(instructions)
    except InfiniteLoop as exc:
        return exc.accumulator


def part2(instructions):
    for new in variants(instructions):
        try:
            accumulator = run_bootcode(list(new))
        except InfiniteLoop:
            continue

        return accumulator


@register(day=8)
def solve(file, verbose):
    parser = ParserPEG(grammar, root_rule_name='instructions', skipws=False)
    parse_tree = parser.parse(file.read())
    instructions = visit_parse_tree(parse_tree, CodeVisitor())
    print('Part 1:', part1(instructions))
    print('Part 2:', part2(instructions))
