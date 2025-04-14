"NeoChart. Core classes."

from icecream import ic

import pathlib

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


def write(item, outfile):
    "Write the YAML of the item into the open file object."
    yaml.safe_dump(item.asdict(), outfile)


def read(filepath_or_stream):
    """Read and parse the file given by its path, or an open file object.
    Returns the Item instance with its subitems.
    """
    if isinstance(filepath_or_stream, (str, pathlib.Path)):
        with open(filepath_or_stream) as infile:
            data = yaml.safe_load(infile)
    else:
        data = yaml.safe_load(filepath_or_stream)
    if len(data) != 1:
        raise ValueError("YAML file must contain exactly one top-level item.")
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

    def update(self, other):
        if isinstance(other, dict):
            self.style.update(other)
        elif isinstance(other, Style):
            self.style.update(other.style)
        else:
            raise ValueError("invalid value for Style update")

    def copy(self):
        return Style(**self.style)

    def asdict(self):
        "Return as a dictionary, which is also suitable for inline attributes."
        data = {}
        for key, value in self.style.items():
            if isinstance(value, Color):
                data[key] = str(value)
            elif isinstance(value, float):
                result[key] = N(value)
            else:
                data[key] = value
        return {"style": data}

    @classmethod
    def parse(cls, data):
        "Parse the data into a Style instance."
        return Style(**data)


class Chart:
    "Abstract chart."

    DEFAULT_STYLE = Style(stroke=Color("black"), fill=Color("white"))
    DEFAULT_PALETTE = Palette(Color("red"), Color("green"), Color("blue"))

    def __init__(self, id=None, title=None, klass=None, style=None, palette=None):
        self.id = id
        self.klass = klass
        self.style = self.DEFAULT_STYLE.copy()
        if style is not None:
            self.style.update(style)
        if palette is None:
            if self.DEFAULT_PALETTE is not None:
                self.palette = self.DEFAULT_PALETTE.copy()
            else:
                self.palette = None
        elif isinstance(palette, Palette):
            self.palette = palette
        elif isinstance(palette, (tuple, list)):
            self.palette = Palette(*palette)
        else:
            raise ValueError("invalid palette specification")

    @property
    def extent(self):
        "Extent of this graphical item."
        return Vector2(0, 0)

    def svg(self):
        "Return the SVG root item with content in minixml representation."
        ext = self.extent
        ori = Vector2(0, 0) - ext / 2
        result = Element(
            "svg",
            xmlns=constants.SVG_XMLNS,
            width=N(ext.x),
            height=N(ext.y),
            viewBox=f"{N(ori.x)} {N(ori.y)} {N(ext.x)} {N(ext.y)}",
        )
        result += self.svg_content()
        return result

    def svg_content(self):
        "Return the SVG content element in minixml representation."
        raise NotImplementedError

    def write(self, filepath_or_stream):
        "Write the this item as SVG root to a new file or the open stream."
        if isinstance(filepath_or_stream, (str, pathlib.Path)):
            with open(filepath_or_stream, "w") as outfile:
                outfile.write(repr(self.svg()))
        else:
            filepath_or_stream.write(repr(self.svg()))

    def write_content(self, filepath_or_stream):
        "Write the the SVG content of this item to a new file or the open stream."
        if isinstance(filepath_or_stream, (str, pathlib.Path)):
            with open(filepath_or_stream, "w") as outfile:
                outfile.write(repr(self.svg_content()))
        else:
            filepath_or_stream.write(repr(self.svg_content()))

    def asdict(self):
        "Return as a dictionary."
        return {self.__class__.__name__.casefold(): self.asdict_content()}

    def asdict_content(self):
        "Return the content as a dictionary."
        data = {}
        if self.id:
            data["id"] = self.id
        if self.klass:
            data["class"] = self.klass
        if self.style:
            data.update(self.style.asdict())
        if self.palette:
            data.update(self.palette.asdict())
        return data

    @classmethod
    def parse(cls, data):
        "Parse the data into an Chart subclass instance."
        try:
            data["klass"] = data.pop("class")
        except KeyError:
            pass
        return cls(**data)
