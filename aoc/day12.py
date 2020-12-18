from __future__ import annotations

from enum import Enum
from math import radians
from typing import Optional

import attr

from .registry import register
from .utils import Vector


class Action(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    LEFT = 'L'
    RIGHT = 'R'
    FORWARD = 'F'


@attr.s(auto_attribs=True)
class Instruction:
    action: Action
    value: int

    @classmethod
    def parse(cls, s: str) -> Instruction:
        s = s.rstrip()
        return cls(Action(s[0]), int(s[1:]))


@attr.s(auto_attribs=True)
class State:
    pos: Vector
    direction: Optional[Vector] = None
    waypoint: Optional[Vector] = None

    def __attrs_post_init__(self):
        if self.direction is None and self.waypoint is None:
            raise ValueError('Either direction or waypoint must be set')

    def apply(self, instruction: Instruction) -> None:
        if instruction.action is Action.NORTH:
            self._move(Vector(0, instruction.value))
        elif instruction.action is Action.SOUTH:
            self._move(Vector(0, -instruction.value))
        elif instruction.action is Action.EAST:
            self._move(Vector(instruction.value, 0))
        elif instruction.action is Action.WEST:
            self._move(Vector(-instruction.value, 0))
        elif instruction.action is Action.LEFT:
            self._rotate(radians(instruction.value))
        elif instruction.action is Action.RIGHT:
            self._rotate(-radians(instruction.value))
        elif instruction.action is Action.FORWARD:
            d = self.direction if self.direction is not None else self.waypoint
            self.pos += d * instruction.value

    def _move(self, vector: Vector) -> None:
        if self.waypoint is None:
            self.pos += vector
        else:
            self.waypoint += vector

    def _rotate(self, theta: float) -> None:
        if self.direction is not None:
            self.direction = self.direction.rotate(theta)
        elif self.waypoint is not None:
            self.waypoint = self.waypoint.rotate(theta)


@register(day=12)
def solve(file, verbose):
    instructions = [Instruction.parse(line) for line in file]

    state1 = State(pos=Vector(0, 0), direction=Vector(1, 0))
    state2 = State(pos=Vector(0, 0), waypoint=Vector(10, 1))

    for instruction in instructions:
        state1.apply(instruction)
        state2.apply(instruction)

    print('Part 1:', int(abs(state1.pos.x) + abs(state1.pos.y)))
    print('Part 2:', int(abs(state2.pos.x) + abs(state2.pos.y)))
