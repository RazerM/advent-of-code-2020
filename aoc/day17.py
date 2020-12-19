from copy import deepcopy
from enum import Enum
from itertools import product, repeat
from typing import Iterator, Tuple

from .itertools import take
from .registry import register


class Cube(Enum):
    ACTIVE = '#'
    INACTIVE = '.'


Position = Tuple[int, int, int]


class PocketDimension:
    def __init__(self, lines, dimensions=3):
        self._active = set()
        self.dimensions = dimensions
        for y, row in enumerate(lines):
            row = row.rstrip()
            for x, cube in enumerate(row):
                key = tuple([x, y, *repeat(0, dimensions - 2)])
                self[key] = Cube(cube)

    def __getitem__(self, item: Position):
        if not isinstance(item, tuple) or len(item) != self.dimensions:
            raise ValueError(f'Must use {self.dimensions} dimensions')

        return Cube.ACTIVE if item in self._active else Cube.INACTIVE

    def __setitem__(self, item: Position, value: Cube) -> None:
        if not isinstance(item, tuple) or len(item) != self.dimensions:
            raise ValueError(f'Must use {self.dimensions} dimensions')

        if value is Cube.INACTIVE:
            self._active.discard(item)
        else:
            self._active.add(item)

    def __str__(self):
        if self.dimensions != 3:
            raise NotImplementedError('Only implemented for 3 dimensions')
        s = ''
        xc, yc, zc = self.coords()
        for i, z in enumerate(zc):
            if i:
                s += '\n'
            s += f'{z=}\n'
            for y in yc:
                for x in xc:
                    s += self[x, y, z].value
                s += '\n'
        return s

    def adjacent(self, pos: Position) -> Iterator[Cube]:
        adjacent_positions = list(
            p for p in product([-1, 0, 1], repeat=self.dimensions) if any(p)
        )
        for offsets in adjacent_positions:
            key = tuple([p + o for p, o in zip(pos, offsets)])
            yield self[key]

    def coords(self, expand=False):
        # list of [min, max] values for each dimension
        ranges = [[None, None]] * self.dimensions
        for pos in self._active:
            for i, dim in enumerate(pos):
                if ranges[i][0] is None or dim < ranges[i][0]:
                    ranges[i][0] = dim
                elif ranges[i][1] is None or dim > ranges[i][1]:
                    ranges[i][1] = dim

        if expand:
            for range_ in ranges:
                range_[0] -= 1
                range_[1] += 1

        return [range(r[0], r[1] + 1) for r in ranges]

    def cycle(self):
        copy = deepcopy(self)

        for pos in product(*self.coords(expand=True)):
            cube = self[pos]
            active_neighbours = (
                c for c in self.adjacent(pos) if c is Cube.ACTIVE
            )
            # we don't need to know if we have more than 4 active neighbours,
            # so we can stop iterating early if we find 4 already
            num_active = sum(take(4, (1 for _ in active_neighbours)))
            if cube is Cube.ACTIVE:
                if num_active < 2 or num_active > 3:
                    copy[pos] = Cube.INACTIVE
            elif cube is Cube.INACTIVE:
                if num_active == 3:
                    copy[pos] = Cube.ACTIVE

        return copy

    @property
    def active(self):
        return len(self._active)


@register(day=17)
def solve(file, verbose):
    lines = list(file)
    pd3 = PocketDimension(lines, dimensions=3)
    pd4 = PocketDimension(lines, dimensions=4)

    for _ in range(6):
        pd3 = pd3.cycle()
    print('Part 1:', pd3.active)

    for _ in range(6):
        pd4 = pd4.cycle()
    print('Part 2:', pd4.active)
