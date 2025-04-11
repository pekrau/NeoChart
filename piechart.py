"NeoChart pie chart."

from base import *


class PieChart(Item):
    "Pie chart."

    DEFAULT_RADIUS = 100.0
    DEFAULT_STYLE = Style(stroke=Color("gray"),
                          stroke_width=2.0)

    def __init__(self, title, radius=None, slices=None, style=None, palette=None):
        super().__init__(style=style, palette=palette)
        self.title = title
        self.radius = self.DEFAULT_RADIUS if radius is None else radius
        self.slices = []
        if slices:
            if isinstance(slices, (tuple, list)):
                for slice in slices:
                    self.append(slice)
            else:
                self.append(slices)

    def append(self, slice):
        if isinstance(slice, (float, int)):
            item = Slice(None, slice)
        elif isinstance(slice, (tuple, list)):
            item = Slice(*slice[0:3])
        elif isinstance(slice, Slice):
            item = slice
        else:
            raise ValueError("invalid slice specification")
        self.slices.append(item)

    def __iadd__(self, other):
        self.append(other)
        return self

    def svg(self):
        result = Element("g", style=self.style)
        circle = Element("circle", r=N(self.radius))
        result += circle
        if self.slices:
            palette = self.palette.cycle()
            total = sum([s.value for s in self.slices])
            for pos, slice in enumerate(self.slices):
                fraction = slice.value / total
                if pos == 0:
                    if slice.start is None:
                        start = Degrees(-90)
                    else:
                        start = slice.start
                    stop = start + fraction * Degrees(360)
                else:
                    start = stop
                    stop = start + fraction * Degrees(360)
                print(start, stop)
                path = Path(Vector2(0, 0))
                p0 = Vector2.from_polar(self.radius, float(start))
                p1 = Vector2.from_polar(self.radius, float(stop))
                path.L(p0).A(self.radius, self.radius, 0, 0, 1, p1).Z()
                wedge = Element("path", d=str(path))
                wedge["style"] = f"fill: {next(palette)};"
                result += wedge
        return result

    @property
    def extent(self):
        return Vector2(2 * self.radius + self.style["stroke-width"],
                       2 * self.radius + self.style["stroke-width"])


class Slice(Item):
    "Slice in a pie chart."

    def __init__(self, title, value, start=None, style=None):
        assert start is None or isinstance(start, Degrees)
        super().__init__(style=style)
        self.title = title
        self.value = value
        self.start = None


if __name__ == "__main__":
    pyramid = PieChart("Pyramid")
    pyramid += Slice("Sky", 45)
    pyramid += ("Sunny side", 30)
    pyramid += Slice("Shady side", 5)
    pyramid += Slice("The rest", 20)
    with open("pyramid.svg", "w") as outfile:
        outfile.write(repr(pyramid.svg_root()))
