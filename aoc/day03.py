import math
from enum import Enum
from typing import Tuple

from .registry import register


class Square(Enum):
    OPEN = '.'
    TREE = '#'


class Grid:
    def __init__(self, lines):
        self._grid = [[Square(s) for s in line.rstrip()] for line in lines]
        self._width = len(self._grid[0])

    def __getitem__(self, item):
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError('Must use grid[x,y]')

        x = item[0] % self._width
        y = item[1]
        return self._grid[y][x]

    def count_trees(self, slope: Tuple[int, int]):
        dx, dy = slope
        x = y = 0
        trees = 0
        while True:
            x += dx
            y += dy

            try:
                s = self[x, y]
            except IndexError:
                return trees

            if s is Square.TREE:
                trees += 1


@register(day=3)
def solve(file, verbose):
    grid = Grid(file)
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    slope_trees = {slope: grid.count_trees(slope) for slope in slopes}
    print('Part 1:', slope_trees[3, 1])
    print('Part 2:', math.prod(slope_trees.values()))
