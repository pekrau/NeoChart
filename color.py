"NeoChart color handling."

import itertools

import webcolors


class Color:

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
            return webcolors.hex_to_name(self.hex)
        except ValueError:
            return self.hex

    @property
    def hex(self):
        return self._hex

    @property
    def rgb(self):
        return tuple(webcolors.hex_to_rgb(self.hex))


class Palette:

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


if __name__ == "__main__":
    for s in ["red", "#a39", "goldenrod", "slategray"]:
        c = Color(s)
        print(c, c.hex, c.rgb)
