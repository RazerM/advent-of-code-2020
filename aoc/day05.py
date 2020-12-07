from __future__ import annotations

from typing import Sequence

from .registry import register


def calculate_seat_id(row: int, col: int) -> int:
    return row * 8 + col


class Seat:
    row: int
    col: int
    id: int

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.id = calculate_seat_id(row, col)

    @classmethod
    def decode(cls, encoded_seat: str) -> Seat:
        row_lower = 0
        row_upper = 127
        col_lower = 0
        col_upper = 7

        for c in encoded_seat:
            row_mid = (row_upper - row_lower) // 2 + row_lower
            col_mid = (col_upper - col_lower) // 2 + col_lower
            if c == 'F':
                row_upper = row_mid
            elif c == 'B':
                row_lower = row_mid + 1
            elif c == 'L':
                col_upper = col_mid
            elif c == 'R':
                col_lower = col_mid + 1

        return Seat(row_lower, col_lower)


def find_my_seat(seats: Sequence[Seat]) -> Seat:
    filled = {(s.row, s.col) for s in seats}
    seat_ids = {s.id for s in seats}

    for row in range(128):
        for col in range(8):
            if (row, col) not in filled:
                seat = Seat(row, col)
                if seat.id - 1 in seat_ids and seat.id + 1 in seat_ids:
                    return seat


@register(day=5)
def solve(file, verbose):
    seats = [Seat.decode(s) for s in file]

    print('Part 1:', max(s.id for s in seats))
    print('Part 2:', find_my_seat(seats).id)
