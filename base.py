"NeoChart. Base classes."

from minixml import Element
from vector2 import Vector2
from color import Color, Palette
from degrees import Degrees


PRECISION = 0.0005

def N(x):
    "Return a compact representation of the numerical value."
    if (x < 0.0 and -x % 1.0 < PRECISION) or x % 1.0 < PRECISION:
        return f"{round(x):d}"
    else:
        return f"{x:.3f}"

class Style:
    "Container of style specifications."

    def __init__(self, **style):
        self.style = {}
        for key, value in style.items():
            self[key] = value

    def __getitem__(self, key):
        return self.style[key]

    def __setitem__(self, key, value):
        self.style[key.replace("_", "-")] = value

    def __str__(self):
        "Return the values as a string appropriate for the 'style' attribute."
        parts = []
        for key, value in self.style.items():
            if isinstance(value, float):
                parts.append(f"{key}: {N(value)};")
            else:
                parts.append(f"{key}: {value};")
        return " ".join(parts)

    def copy(self):
        return Style(**self.style)


class Item:
    "Abstract graphical item."

    DEFAULT_STYLE = Style()
    DEFAULT_PALETTE = Palette(Color("#4c78a8"),
                              Color("#9ecae9"),
                              Color("#f58518"),
                              Color("#ffbf79"))

    def __init__(self, style=None, palette=None):
        self.style = self.DEFAULT_STYLE.copy()
        if style is not None:
            self.style.update(style)
        if palette is  None:
            self.palette = self.DEFAULT_PALETTE.copy()
        else:
            self.palette = palette

    @property
    def extent(self):
        "Extent of this graphical item."
        return Vector2(0, 0)

    def svg_root(self):
        "Return the SVG root item with content in minixml representation."
        extent = self.extent
        origin = Vector2(0, 0) - extent / 2
        result = Element(
            "svg",
            width=N(extent.x),
            height=N(extent.y),
            viewBox=f"{N(origin.x)} {N(origin.y)} {N(extent.x)} {N(extent.y)}")
        result.append(self.svg())
        return result

    def svg(self):
        "Return the SVG content element in minixml representation."
        raise NotImplementedError


class Path:
    "SVG path synthesizer."

    def __init__(self, v0, *v):
        "Moveto v0, then lineto any v's. Absolute coordinates."
        self.parts = []
        self.M(v0, *v)

    def __str__(self):
        return " ".join(self.parts)

    def M(self, v0, *v):
        "Moveto, then lineto any v's. Absolute coordinates."
        self._add("M", v0, *v, concatenate=False)
        return self

    def m(self, v0, *v):
        "Moveto, then lineto any v's. Relative coordinates."
        self._add("m", v0, *v, concatenate=False)
        return self

    def L(self, v0, *v):
        "Lineto. Absolute coordinates."
        self._add("L", v0, *v)
        return self

    def l(self, v0, *v):
        "Lineto. Relative coordinates."
        self._add("l", v0, *v)
        return self

    def H(self, x):
        "Horizontal lineto. Absolute coordinates."
        self.parts.append(f"H {x:.5g}")
        return self

    def h(self, x):
        "Horizontal lineto. Relative coordinates."
        self.parts.append(f"h {x:.5g}")
        return self

    def V(self, x):
        "Vertical lineto. Absolute coordinates."
        self.parts.append(f"V {x:.5g}")
        return self

    def v(self, x):
        "Vertical lineto. Relative coordinates."
        self.parts.append(f"v {x:.5g}")
        return self

    def C(self, v1, v2, v):
        "Cubic Beziér curveto. Absolute coordinates."
        self._add("C", v1, v2, v)
        return self

    def c(self, v1, v2, v):
        "Cubic Beziér curveto. Relative coordinates."
        self._add("c", v1, v2, v)
        return self

    def S(self, v2, v):
        "Shorthand cubic Beziér curveto. Absolute coordinates."
        self._add("S", v2, v)
        return self

    def s(self, v2, v):
        "Shorthand cubic Beziér curveto. Relative coordinates."
        self._add("s", v2, v)
        return self

    def Q(self, v1, v):
        "Quadratic  Beziér curveto. Absolute coordinates."
        self._add("Q", v1, v)
        return self

    def q(self, v2, *v):
        "Quadratic Beziér curveto. Relative coordinates."
        self._add("q", v1, v)
        return self

    def T(self, v1, *v):
        "Shorthand quadratic  Beziér curveto. Absolute coordinates."
        self._add("T", v1, v)
        return self

    def t(self, v1, *v):
        "Shorthand quadratic Beziér curveto. Relative coordinates."
        self._add("t", v1, v)
        return self

    def A(self, xr, yr, xrot, laf, sf, v):
        "Elliptical arc. Absolute coordinates."
        self.parts.append(f"A {N(xr)} {N(yr)} {N(xrot)} {N(laf)} {N(sf)} {N(v.x)} {N(v.y)}")
        return self

    def a(self, rx, ry, xrot, laf, sf, v):
        "Elliptical arc. Relative coordinates."
        self.parts.append(f"a {N(xr)} {N(yr)} {N(xrot)} {N(laf)} {N(sf)} {N(v.x)} {N(v.y)}")
        return self

    def Z(self):
        "Close path."
        self.parts.append("Z")

    def _add(self, command, *v, concatenate=True):
        bits = []
        if not (concatenate and self.parts[-1][0] == command):
            bits.append(command)
        bits.append(" ".join([f"{N(w.x)} {N(w.y)}" for w in v]))
        self.parts.append(" ".join(bits))


if __name__ == "__main__":
    for x in [0.0, 0.001, -0.001, 0.0007, -0.0007, 1000.001, 1000.0007, -1000.001, -1000.0007]:
        print(x, N(x))
