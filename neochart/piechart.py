"NeoChart pie chart."

import collections

import utils
from chart import *


__all__ = ["Piechart", "Slice"]


Slice = collections.namedtuple(
    "Slice", ["value", "label", "style"], defaults=[None, None]
)


class Piechart(Chart):
    "Pie chart."

    DEFAULT_RADIUS = 100.0
    DEFAULT_STYLE = Style(
        stroke=Color("gray"),
        stroke_width=2,
        fill=Color("white"),
        palette=Palette("red", "green", "blue"),
    )

    def __init__(
        self,
        id=None,
        klass=None,
        radius=None,
        start=None,
        total=None,
        style=None,
        slices=None,
    ):
        super().__init__(id=id, klass=klass, style=style)
        self.radius = radius if radius is not None else self.DEFAULT_RADIUS
        if isinstance(start, (int, float)):
            self.start = Degrees(start)
        else:
            self.start = start
        self.total = total
        self.slices = []
        if slices:
            for slice in slices:
                self.append(slice)

    def append(self, slice):
        if isinstance(slice, Slice):
            item = slice
        elif isinstance(slice, (float, int)):
            item = Slice(slice)
        elif isinstance(slice, (tuple, list)) and len(slice) == 2:
            item = Slice(*slice)
        elif isinstance(slice, dict) and "value" in slice:
            try:
                style = Style(**slice["style"])
            except KeyError:
                style = None
            item = Slice(slice["value"], slice.get("label"), style)
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
        result = super().svg_content()
        self.style.setattrs(result, "stroke", "stroke-width", "fill")
        circle = Element("circle", r=utils.N(self.radius))
        result += circle
        if self.slices:
            try:
                palette = self.style["palette"].cycle()
            except KeyError:
                palette = None
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
                    elem["fill"] = str(slice.style["fill"])
                except (TypeError, KeyError):
                    if palette:
                        elem["fill"] = str(next(palette))
                result += elem
        return result

    def as_dict_content(self):
        "Return content as a dictionary of basic YAML values."
        data = super().as_dict_content()
        data["radius"] = self.radius
        data["start"] = None if self.start is None else self.start.degrees
        data["slices"] = []
        for slice in self.slices:
            d = dict(value=slice.value)
            if slice.label:
                d["label"] = slice.label
            if slice.style:
                d.update(slice.style.as_dict())
            data["slices"].append(d)
        return data


add_chart(Piechart)
