"Angle specified in degrees. Immutable."

import math


class Degrees:
    "Handle angle specified in degrees, yields value in radians."

    @classmethod
    def from_radians(cls, radians):
        assert isinstance(radians, (float, int))
        return Degrees(180.0 * radians / math.pi)

    def __init__(self, degrees):
        assert isinstance(degrees, (float, int))
        self._degrees = degrees

    def __add__(self, other):
        assert isinstance(other, (float, int, Degrees))
        if isinstance(other, Degrees):
            return Degrees(self.degrees + other.degrees)
        else:
            return Degrees(self.degrees + other)

    def __sub__(self, other):
        assert isinstance(other, (float, int, Degrees))
        if isinstance(other, Degrees):
            return Degrees(self.degrees - other.degrees)
        else:
            return Degrees(self.degrees - other)

    def __mul__(self, other):
        assert isinstance(other, (float, int))
        return Degrees(other * self.degrees)

    def __rmul__(self, other):
        assert isinstance(other, (float, int))
        return Degrees(other * self.degrees)

    def __truediv__(self, other):
        assert isinstance(other, (float, int))
        return Degrees(self.degrees / other)

    def __neg__(self):
        return Degrees(- self.degrees)

    def __float__(self):
        "Angle in radians."
        return self.degrees * math.pi / 180.0

    def __repr__(self):
        return f"Degrees({self.degrees})"

    @property
    def degrees(self):
        return self._degrees

    @property
    def radians(self):
        return float(self)

    def normalized(self):
        "Return the angle normalized to within [-180, 180]."
        degrees = self.degrees % 360.0
        if degrees > 180.0:
            degrees -= 360.0
        if degrees < -180.0:
            degrees += 360.0
        return Degrees(degrees)


if __name__ == "__main__":
    a = Degrees(90)
    print(a)
    print(a + 45)
    print(2 * a)
    print(Degrees(350).normalized())
    print(Degrees(-350).normalized())
