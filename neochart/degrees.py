"Angle specified in degrees. Immutable."

from __future__ import annotations

import math
import functools

from typing import Union, Any


@functools.total_ordering
class Degrees:
    "Handle angle specified in degrees, yields value in radians."

    @classmethod
    def from_radians(cls, radians: float) -> Degrees:
        assert isinstance(radians, (float, int))
        return Degrees(180.0 * radians / math.pi)

    def __init__(self, degrees: Union[int, float]):
        self._degrees = degrees

    def __add__(self, other: Union[int, float, Degrees]) -> Degrees:
        if isinstance(other, Degrees):
            return Degrees(self.degrees + other.degrees)
        else:
            return Degrees(self.degrees + other)

    def __sub__(self, other: Union[int, float, Degrees]) -> Degrees:
        if isinstance(other, Degrees):
            return Degrees(self.degrees - other.degrees)
        else:
            return Degrees(self.degrees - other)

    def __mul__(self, other: Union[int, float]) -> Degrees:
        return Degrees(other * self.degrees)

    def __rmul__(self, other: Union[int, float]) -> Degrees:
        return Degrees(other * self.degrees)

    def __truediv__(self, other: Union[int, float]) -> Degrees:
        return Degrees(self.degrees / other)

    def __lt__(self, other: Degrees) -> bool:
        return self._degrees < other._degrees

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Degrees):
            return self._degrees == other._degrees
        elif isinstance(other, (int, float)):
            return self._degrees == other
        else:
            return False

    def __neg__(self) -> Degrees:
        return Degrees(-self.degrees)

    def __float__(self) -> float:
        "Angle in radians."
        return self.degrees * math.pi / 180.0

    def __repr__(self) -> str:
        return f"Degrees({self.degrees:g})"

    @property
    def degrees(self) -> float:
        return self._degrees

    @property
    def radians(self) -> float:
        return float(self)

    def normalized(self) -> Degrees:
        "Return the angle normalized to within [-180, 180]."
        degrees = self.degrees % 360.0
        if degrees > 180.0:
            degrees -= 360.0
        if degrees < -180.0:
            degrees += 360.0
        return Degrees(degrees)
