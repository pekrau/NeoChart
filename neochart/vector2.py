"Two-dimensional vector (x, y). Immutable."

from __future__ import annotations

import math

from typing import Union


class Vector2:
    "Two-dimensional vector (x, y). Immutable."

    @classmethod
    def from_polar(cls, r: Union[int, float], phi: Union[int, float]) -> Vector2:
        "Return a Vector2 instance defined by polar coordinates (radians)."
        return Vector2(r * math.cos(phi), r * math.sin(phi))

    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self._x = x
        self._y = y

    @property
    def x(self) -> Union[int, float]:
        return self._x

    @property
    def y(self) -> Union[int, float]:
        return self._y

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"Vector2({self.x:g}, {self.y:g})"

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __truediv__(self, other: Union[int, float]) -> Vector2:
        return Vector2(self.x / other, self.y / other)

    def __rmul__(self, other: Union[int, float]) -> Vector2:
        return Vector2(other * self.x, other * self.y)

    def __float__(self) -> float:
        return abs(self)

    def __complex__(self) -> complex:
        return complex(self.x, self.y)

    @property
    def normalized(self) -> Vector2:
        length = abs(self)
        return Vector2(self.x / length, self.y / length)

    @property
    def r(self) -> float:
        "Return the radius part of the polar coordinates."
        return abs(self)

    @property
    def phi(self) -> float:
        "Return the angle part of the polar coordinates (radians)."
        return math.atan2(self.y, self.x)

    @property
    def polar(self) -> tuple[float, float]:
        "Return the tuple (r, phi) for this instance (radians)."
        return (self.r, self.phi)
