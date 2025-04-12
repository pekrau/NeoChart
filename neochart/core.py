"NeoChart. Core classes."

from pathlib import Path

import yaml

import constants
from color import Color, Palette
from degrees import Degrees
from minixml import Element
from vector2 import Vector2
from utils import N

from icecream import ic


parse_lookup = {}


def read(filepath_or_stream):
    """Read and parse the file given by its path, or an open file object.
    Returns the Item instance with its subitems.
    """
    if isinstance(filepath_or_stream, (str, Path)):
        with open(filepath_or_stream) as infile:
            data = yaml.safe_load(infile)
    else:
        data = yaml.safe_load(filepath_or_stream)
    if len(data) != 1:
        raise ValueError("YAML data must contain exactly one item.")
    return parse(*data.popitem())


def parse(key, data):
    try:
        parse = parse_lookup[key]
    except KeyError:
        raise ValueError(f"cannot parse unknown item in YAML data: '{key}'")
    return parse(data)


class Style:
    "Container of style specifications."

    def __init__(self, **styles):
        self.style = {}
        for key, value in styles.items():
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

    def update(self, other):
        if isinstance(other, dict):
            self.style.update(other)
        elif isinstance(other, Style):
            self.style.update(other.style)
        else:
            raise ValueError("invalid value for Style update")

    def copy(self):
        return Style(**self.style)

    def data(self):
        "Return this item as a dictionary."
        data = {}
        for key, value in self.style.items():
            if isinstance(value, Color):
                data[key] = str(value)
            else:
                data[key] = value
        return {"style": data}

    @classmethod
    def parse(cls, data):
        "Parse the data content into a Style instance."
        return Style(**data)


# Add the parse function for Style.
parse_lookup["style"] = Style.parse


class Item:
    "Abstract graphical item."

    DEFAULT_STYLE = Style(stroke=Color("black"), fill=Color("cyan"))
    DEFAULT_PALETTE = Palette(Color("red"), Color("green"), Color("blue"))

    def __init__(self, style=None, palette=None):
        self.style = self.DEFAULT_STYLE.copy()
        if style is not None:
            self.style.update(style)
        if palette is None:
            if self.DEFAULT_PALETTE is not None:
                self.palette = self.DEFAULT_PALETTE.copy()
            else:
                self.palette = None
        else:
            self.palette = palette

    @property
    def extent(self):
        "Extent of this graphical item."
        return Vector2(0, 0)

    def svg(self):
        "Return the SVG root item with content in minixml representation."
        extent = self.extent
        origin = Vector2(0, 0) - extent / 2
        result = Element(
            "svg",
            xmlns=constants.SVG_XMLNS,
            width=N(extent.x),
            height=N(extent.y),
            viewBox=f"{N(origin.x)} {N(origin.y)} {N(extent.x)} {N(extent.y)}",
        )
        result.append(self.svg_content())
        return result

    def svg_content(self):
        "Return the SVG content element in minixml representation."
        raise NotImplementedError

    def data(self):
        "Return this item as a dictionary."
        data = {}
        if self.style:
            data = self.style.data()
        if self.palette:
            data.update(self.palette.data())
        data.update(self.data_content())
        return {self.__class__.__name__.casefold(): data}

    def data_content(self):
        "Return the data content of this item as a dictionary."
        return {}

    def write(self, outfile):
        "Write the YAML of this item into the open file object."
        yaml.safe_dump(self.data(), outfile)

    @classmethod
    def parse(cls, data):
        raise NotImplementedError
