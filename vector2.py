"Two-dimensional vector (x, y). Immutable."

import math


class Vector2:
    "Two-dimensional vector (x, y). Immutable."

    @classmethod
    def from_polar(cls, r, phi):
        "Return a Vector2 instance defined by polar coordinates (radians)."
        return Vector2(r * math.cos(phi), r * math.sin(phi))

    def __init__(self, x, y):
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("invalid instance class for addition")
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError("invalid instance class for subtraction")
        return Vector2(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):        
        if not isinstance(other, (int, float)):
            raise ValueError("division requires int or float")
        return Vector2(self.x / other, self.y / other)

    def __rmul__(self, other):
        if not isinstance(other, (int, float)):
            raise ValueError("multiplication requires int or float")
        return Vector2(other * self.x, other * self.y)

    def __float__(self):
        return abs(self)

    def __complex__(self):
        return complex(self.x, self.y)

    @property
    def normalized(self):
        length = abs(self)
        return Vector2(self.x / length, self.y / length)

    @property
    def r(self):
        "Return the radius part of the polar coordinates."
        return abs(self)

    @property
    def phi(self):
        "Return the angle part of the polar coordinates (radians)."
        return math.atan2(self.y, self.x)

    @property
    def polar(self):
        "Return the tuple (r, phi) for this instance (radians)."
        return (self.r, self.phi)


if __name__ == "__main__":
    from degrees import Degrees
    # v = Vector2(1.0, 3.0)
    # print(abs(v))
    # print(-v)
    # print(v-v)
    # print(v.normalized)
    # print(abs(v.normalized))
    for phi in [0, 45, 90+45, 180, 180+45, 180+90+45]:
        v = Vector2.from_polar(1.0, Degrees(phi))
        r, p = v.polar
        print(phi, v, (r, Degrees.from_radians(p).degrees))
