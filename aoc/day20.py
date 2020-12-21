import re

from .registry import register


class Tile:
    def __init__(self, lines):
        it = iter(lines)
        match = re.match(r'Tile\s+(\d+):', next(it))
        self.id = int(match.group(1))

        self._grid = []
        for line in it:
            line = line.rstrip()

            if not line:
                break

            self._grid.append(list(line))

    def edges(self):
        yield ''.join(self._grid[0])
        yield ''.join(self._grid[-1])
        left = ''
        right = ''
        for row in self._grid:
            left += row[0]
            right += row[-1]
        yield left
        yield right


class UniversalEdge:
    """Wrapper type to help compare edges regardless of orientation"""
    def __init__(self, edge):
        self._edge = edge

    def __hash__(self):
        cls = type(self)
        return hash(tuple([cls, *sorted([self._edge, self._edge[::-1]])]))

    def __eq__(self, other):
        if isinstance(other, UniversalEdge):
            return hash(self) == hash(other)
        return NotImplemented


@register(day=20)
def solve(file, verbose):
    tiles = []
    while True:
        try:
            tile = Tile(file)
        except StopIteration:
            break
        else:
            tiles.append(tile)

    tile_edges = {
        tile.id: {UniversalEdge(e) for e in tile.edges()} for tile in tiles
    }

    m = 1
    for id_, edges in tile_edges.items():
        x = edges & set.union(*(e for i, e in tile_edges.items() if i != id_))
        if len(x) == 2:
            m *= id_
    print('Part 1:', m)
