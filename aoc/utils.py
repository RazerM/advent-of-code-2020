from math import cos, sin
from numbers import Number

import attr


@attr.s(auto_attribs=True, frozen=True)
class Vector:
    x: float
    y: float

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(self.x * other, self.y * other)

        return NotImplemented

    def rotate(self, theta):
        sin_theta = sin(theta)
        cos_theta = cos(theta)
        return Vector(
            self.x * cos_theta - self.y * sin_theta,
            self.x * sin_theta + self.y * cos_theta,
        )
