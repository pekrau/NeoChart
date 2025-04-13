"NeoChart pie chart."

from core import *
from utils import Path

from icecream import ic


class Piechart(Item):
    "Pie chart."

    DEFAULT_RADIUS = 100.0
    DEFAULT_STYLE = Style(stroke=Color("gray"), stroke_width=2, fill=Color("white"))
    DEFAULT_PALETTE = Palette(
        Color("#4c78a8"), Color("#9ecae9"), Color("#f58518"), Color("#ffbf79")
    )

    def __init__(
        self,
        title=None,
        radius=None,
        start=None,
        total=None,
        style=None,
        palette=None,
        slices=None,
    ):
        super().__init__(style=style, palette=palette)
        self.title = title
        self.radius = radius if radius is not None else self.DEFAULT_RADIUS
        if isinstance(start, (int, float)):
            self.start = Degrees(start)
        else:
            self.start = start
        self.total = total
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

    @property
    def extent(self):
        return Vector2(
            2 * self.radius + self.style["stroke-width"],
            2 * self.radius + self.style["stroke-width"],
        )

    def svg_content(self):
        "Return the SVG content element in minixml representation."
        result = Element("g", **self.style.attrs())
        result["class"] = "piechart"
        circle = Element("circle", r=N(self.radius))
        result += circle
        if self.slices:
            palette = self.palette.cycle()
            total = sum([s.value for s in self.slices])
            if self.total:
                total = max(total, self.total)
            stop = self.start - Degrees(90) if self.start else Degrees(-90)
            for slice in self.slices:
                fraction = slice.value / total
                start = stop
                stop = start + fraction * Degrees(360)
                path = Path(Vector2(0, 0))
                p0 = Vector2.from_polar(self.radius, float(start))
                p1 = Vector2.from_polar(self.radius, float(stop))
                lof = 1 if stop - start > Degrees(180) else 0
                path.L(p0).A(self.radius, self.radius, 0, lof, 1, p1).Z()
                elem = Element("path", d=str(path))
                try:
                    color = slice.style["fill"]
                except KeyError:
                    color = next(palette)
                elem["fill"] = str(color)
                result += elem
        return result

    def data_content(self):
        "Return the data content of this item as a dictionary."
        return dict(
            title=self.title,
            radius=self.radius,
            start=None if self.start is None else self.start.degrees,
            slices=[s.data() for s in self.slices],
        )

    @classmethod
    def parse(cls, data):
        "Parse the data content into a Piechart instance."
        kwargs = dict(
            title=data.get("title"),
            radius=data.get("radius"),
            start=data.get("start"),
            total=data.get("total"),
            slices=[Slice.parse(d) for d in data.get("slices") or []],
        )
        try:
            kwargs["style"] = Style.parse(data["style"])
        except KeyError:
            pass
        try:
            kwargs["palette"] = Palette.parse(data["style"])
        except KeyError:
            pass
        return Piechart(**kwargs)


class Slice(Item):
    "Slice in a pie chart."

    DEFAULT_STYLE = Style()
    DEFAULT_PALETTE = None

    def __init__(self, title, value, style=None):
        super().__init__(style=style)
        self.title = title
        self.value = value

    def data_content(self):
        return {"title": self.title, "value": self.value}

    @classmethod
    def parse(cls, data):
        slice = data["slice"]
        kwargs = dict(title=slice["title"], value=slice["value"])
        try:
            kwargs["style"] = Style.parse(slice["style"])
        except KeyError:
            pass
        return Slice(**kwargs)


add_parse_lookup(Piechart)


if __name__ == "__main__":
    import io

    pyramid = Piechart("Pyramid", start=Degrees(132))
    pyramid += Slice("Shady side", 10)
    pyramid += ("Sunny side", 15)
    pyramid += Slice("Sky", 70)
    with open("pyramid.svg", "w") as outfile:
        outfile.write(repr(pyramid.svg()))
    contents1 = pyramid.data()
    buffer = io.StringIO()
    write(pyramid, buffer)
    buffer.seek(0)
    with open("pyramid.yaml", "w") as outfile:
        outfile.write(buffer.read())
    buffer.seek(0)
    pyramid = read(buffer)
    contents2 = pyramid.data()
    assert contents1 == contents2
