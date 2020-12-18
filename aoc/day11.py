from __future__ import annotations

from copy import deepcopy
from enum import Enum
from itertools import product
from typing import Iterator, Optional, Tuple

from .itertools import take
from .registry import register


class Tile(Enum):
    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'


Position = Tuple[int, int]

adjacent_positions = list(p for p in product([-1, 0, 1], repeat=2) if p != (0, 0))


class Layout:
    def __init__(self, lines):
        self._grid = [[Tile(s) for s in line.rstrip()] for line in lines]
        self._width = len(self._grid[0])
        self._height = len(self._grid)

    def __getitem__(self, item: Position):
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError('Must use grid[x,y]')

        x, y = item

        if x < 0 or y < 0:
            raise IndexError('positions must be positive')

        return self._grid[y][x]

    def __setitem__(self, item: Position, value: Tile) -> None:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError('Must use grid[x,y]')

        x, y = item
        self._grid[y][x] = value

    def positions(self) -> Iterator[Position]:
        for y in range(self._height):
            for x in range(self._width):
                yield x, y

    def fill(self, *, simple=True) -> Optional[Layout]:
        copy = None

        for x, y in self.positions():
            if new_tile := self.apply_rule((x, y), simple=simple):
                if copy is None:
                    copy = deepcopy(self)
                copy[x, y] = new_tile

        return copy

    def adjacent(self, item: Position) -> Iterator[Tile]:
        ox, oy = item

        for dx, dy in adjacent_positions:
            x = ox + dx
            y = oy + dy
            try:
                yield self[x, y]
            except IndexError:
                continue

    def visible(self, item: Position) -> Iterator[Tile]:
        ox, oy = item

        for dx, dy in adjacent_positions:
            x, y = ox, oy
            while True:
                x += dx
                y += dy
                try:
                    tile = self[x, y]
                except IndexError:
                    break

                if tile is Tile.FLOOR:
                    continue
                else:
                    yield tile
                    break

    def apply_rule(self, item: Position, *, simple=True) -> Optional[Tile]:
        tile = self[item]
        occupied_threshold = 4 if simple else 5

        if tile is Tile.FLOOR:
            return

        seats = self.adjacent(item) if simple else self.visible(item)
        occupied = (1 for t in seats if t is Tile.OCCUPIED)

        if tile is Tile.EMPTY:
            if not any(occupied):
                return Tile.OCCUPIED
        elif tile is Tile.OCCUPIED:
            if len(take(occupied_threshold, occupied)) == occupied_threshold:
                return Tile.EMPTY

    def occupied(self) -> int:
        return sum(self[pos] is Tile.OCCUPIED for pos in self.positions())

    def __str__(self):
        s = ''
        for row in self._grid:
            for col in row:
                s += col.value
            s += '\n'
        return s.rstrip()


def count_occupied(layout: Layout, *, simple) -> int:
    while True:
        if new_layout := layout.fill(simple=simple):
            layout = new_layout
        else:
            return layout.occupied()


@register(day=11)
def solve(file, verbose):
    layout = Layout(file)

    print('Part 1:', count_occupied(layout, simple=True))
    print('Part 2:', count_occupied(layout, simple=False))
