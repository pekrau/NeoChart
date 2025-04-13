"NeoChart color handling."

import itertools

import webcolors


class Color:
    "Color defined by hex, name or rgb triple."

    def __init__(self, *values):
        if len(values) == 1 and isinstance(values[0], str):
            if values[0].startswith("#"):
                self._hex = webcolors.normalize_hex(values[0])
            else:
                self._hex = webcolors.name_to_hex(values[0])
        elif len(values) == 1 and isinstance(values[0], Color):
            self._hex = values[0].hex
        elif len(values) == 3 and all([isinstance(v, int) for v in values]):
            self._hex = webcolors.rgb_to_hex(values)
        else:
            raise ValueError("invalid color specification")

    def __str__(self):
        "Return the named color, if any, or the hex code."
        try:
            return self.name
        except ValueError:
            return self.hex

    @property
    def hex(self):
        return self._hex

    @property
    def rgb(self):
        return tuple(webcolors.hex_to_rgb(self.hex))

    @property
    def name(self):
        "Return the name for the color. Raise ValueError if none."
        return webcolors.hex_to_name(self.hex)


class Palette:
    "Ordered set of colors."

    def __init__(self, *colors):
        self.colors = []
        for color in colors:
            self.add(color)

    def __iadd__(self, other):
        self.add(other)
        return self

    def add(self, color):
        self.colors.append(color)

    def copy(self):
        return Palette(*self.colors)

    def cycle(self):
        "Return an eternally cycling iterator over the current colors."
        return itertools.cycle(self.colors[:])

    def data(self):
        "Return this item as a dictionary."
        return {"palette": [str(c) for c in self.colors]}

    @classmethod
    def parse(cls, data):
        "Parse the data content into a Palette instance."
        return Palette(*[Color(h) for h in data["palette"]])


if __name__ == "__main__":
    palette = Palette(
        Color("red"), Color("#a39"), Color("goldenrod"), Color("slategray")
    )
    palette_cycle = palette.cycle()
    for i in range(8):
        c = next(palette_cycle)
        print(c, c.hex, c.rgb)
