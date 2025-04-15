"NeoChart. Core classes; Chart, Style."

import copy
import io
import pathlib

import cairosvg
import yaml

import constants
from color import Color, Palette
from degrees import Degrees
from minixml import Element
from vector2 import Vector2
from utils import N, Path


__all__ = [
    "Chart",
    "Style",
    "Degrees",
    "Element",
    "Vector2",
    "Color",
    "Palette",
    "Path",
    "write",
    "read",
    "parse",
    "add_chart",
]

_chart_lookup = {}


def add_chart(cls):
    "Add the chart class to the parse lookup table."
    if not issubclass(cls, Chart):
        raise ValueError
    _chart_lookup[cls.__name__.casefold()] = cls.parse


def get_parse_function(name):
    "Get the parse function for the chart name."
    try:
        return _chart_lookup[name]
    except KeyError:
        raise ValueError(f"no parse function for item '{key}' in YAML data")


def write(chart, outfile):
    "Write the YAML of the chart into the open file object."
    yaml.safe_dump(chart.as_dict(), outfile)


def read(filepath_or_stream):
    """Read and parse the file given by its path, or an open file object.
    Returns a Chart instance.
    """
    if isinstance(filepath_or_stream, (str, pathlib.Path)):
        with open(filepath_or_stream) as infile:
            data = yaml.safe_load(infile)
    else:
        data = yaml.safe_load(filepath_or_stream)
    if len(data) != 1:
        raise ValueError("YAML file must contain exactly one top-level chart.")
    return parse(*data.popitem())


def parse(key, data):
    return _chart_lookup[key](data)


class Style:
    "Container of style specifications."

    def __init__(self, **styles):
        self.style = {}
        for key, value in styles.items():
            self[key] = value

    def __len__(self):
        return len(self.style)

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

    def set(self, key, value):
        if key == "palette" and isinstance(value, (tuple, list)):
            self.style["palette"] = Palette(*value)
        else:
            self.style[key] = copy.deepcopy(value)

    def update(self, other):
        if isinstance(other, dict):
            for key, value in other.items():
                self.set(key, value)
        elif isinstance(other, Style):
            self.update(other.style)
        else:
            raise ValueError("invalid value for Style update")

    def setattrs(self, elem, *attrnames):
        "Set the attributes given by the names, if existing, in the element."
        for attrname in attrnames:
            try:
                elem[attrname] = self.style[attrname]
            except KeyError:
                pass

    def as_dict(self):
        "Return as a dictionary of basic YAML values."
        data = {}
        for key, value in self.style.items():
            if isinstance(value, Color):
                data[key] = str(value)
            elif isinstance(value, Palette):
                data[key] = [str(c) for c in value.colors]
            elif isinstance(value, float):
                result[key] = N(value)
            else:
                data[key] = value
        return {"style": data}


class Chart:
    "Abstract chart."

    DEFAULT_STYLE = Style(
        stroke=Color("black"),
        fill=Color("white"),
        palette=Palette("red", "green", "blue"),
    )

    def __init__(self, id=None, klass=None, style=None):
        self.id = id
        self.klass = klass
        self.style = copy.deepcopy(self.DEFAULT_STYLE)
        if style is not None:
            self.style.update(style)

    @property
    def extent(self):
        "Extent of this chart."
        return Vector2(0, 0)

    def svg(self):
        "Return the SVG root element with content in minixml representation."
        origin = Vector2(0, 0) - (extent := self.extent) / 2
        result = Element(
            "svg",
            xmlns=constants.SVG_XMLNS,
            width=N(extent.x),
            height=N(extent.y),
            viewBox=f"{N(origin.x)} {N(origin.y)} {N(extent.x)} {N(extent.y)}",
        )
        result += self.svg_content()
        return result

    def svg_content(self):
        "Return the SVG content element in minixml representation."
        result = Element("g")
        if self.id:
            result["id"] = self.id
        if self.klass:
            result["class"] = self.klass
        return result

    def write(self, filepath_or_stream):
        "Write the this chart as SVG root to a new file or the open stream."
        if isinstance(filepath_or_stream, (str, pathlib.Path)):
            with open(filepath_or_stream, "w") as outfile:
                outfile.write(repr(self.svg()))
        else:
            filepath_or_stream.write(repr(self.svg()))

    def write_content(self, filepath_or_stream):
        "Write the the SVG content of this chart to a new file or the open stream."
        if isinstance(filepath_or_stream, (str, pathlib.Path)):
            with open(filepath_or_stream, "w") as outfile:
                outfile.write(repr(self.svg_content()))
        else:
            filepath_or_stream.write(repr(self.svg_content()))

    def write_png(self, filepath_or_stream, scale=1.0):
        "Write this chart as a PNG image to a new file or the open stream."
        assert scale > 0.0
        if isinstance(filepath_or_stream, (str, pathlib.Path)):
            with open(filepath_or_stream, "wb") as outfile:
                inputfile = io.StringIO(repr(self.svg()))
                outfile.write(cairosvg.svg2png(file_obj=inputfile, scale=scale))
        else:
            inputfile = io.StringIO(repr(self.svg()))
            filepath_or_stream.write(cairosvg.svg2png(file_obj=inputfile, scale=scale))

    def as_dict(self):
        "Return as a dictionary of basic YAML values."
        return {self.__class__.__name__.casefold(): self.as_dict_content()}

    def as_dict_content(self):
        "Return the content as a dictionary of basic YAML values."
        data = {}
        if self.id:
            data["id"] = self.id
        if self.klass:
            data["class"] = self.klass
        if self.style:
            data.update(self.style.as_dict())
        return data

    @classmethod
    def parse(cls, data):
        "Parse the data into an Chart subclass instance."
        try:
            data["klass"] = data.pop("class")
        except KeyError:
            pass
        return cls(**data)
