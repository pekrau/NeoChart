"NeoChart. Command line tool to convert YAML file to SVG or PNG."

import io
from pathlib import Path

import cairosvg
import click

import core
import piechart


@click.group()
def cli():
    pass


@cli.command()
@click.option("-i", "--indent", default=2)
@click.argument("infilepath", nargs=1, required=True)
@click.argument("outfilepath", nargs=1, required=False)
def svg(indent, infilepath, outfilepath=None):
    if not outfilepath:
        outfilepath = Path(infilepath).with_suffix(".svg")
    with open(outfilepath, "w") as outfile:
        core.read(infilepath).svg().write(outfile, indent=indent)


@cli.command()
@click.option("-s", "--scale", default=1.0, type=float)
@click.argument("infilepath", nargs=1, required=True)
@click.argument("outfilepath", nargs=1, required=False)
def png(scale, infilepath, outfilepath=None):
    if not outfilepath:
        outfilepath = Path(infilepath).with_suffix(".png")
    buffer = io.StringIO(repr(core.read(infilepath).svg()))
    with open(outfilepath, "wb") as outfile:
        outfile.write(cairosvg.svg2png(file_obj=buffer, scale=scale))


if __name__ == "__main__":
    cli()
