"Test NeoChart."

from common import *
from cli import write_png


if __name__ == "__main__":
    import io

    pyramid = Piechart(title="Pyramid", start=Degrees(132))
    pyramid += Slice(10, "Shady side")
    pyramid += (15, "Sunny side")
    pyramid += Slice(70, "Sky")
    pyramid.write("pyramid.svg")
    contents1 = pyramid.asdict()
    buffer = io.StringIO()
    write(pyramid, buffer)
    buffer.seek(0)
    with open("pyramid.yaml", "w") as outfile:
        outfile.write(buffer.read())
    buffer.seek(0)
    pyramid = read(buffer)
    contents2 = pyramid.asdict()
    assert contents1 == contents2
    write_png(2.0, "pyramid.yaml")
