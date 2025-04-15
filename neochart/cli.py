"NeoChart. Command line tool to convert YAML file to SVG or PNG."

import io
import pathlib

import cairosvg
import click

from common import *


@click.group()
def cli():
    pass


@cli.command()
@click.option("-i", "--indent", default=2, type=int)
@click.argument("infilepath", nargs=1, required=True)
@click.argument("outfilepath", nargs=1, required=False)
def svg(indent, infilepath, outfilepath=None):
    "Convert NeoChart YAML to SVG file."
    write_svg(indent, infilepath, outfilepath)


def write_svg(infilepath, outfilepath=None, indent=2):
    if not outfilepath:
        outfilepath = pathlib.Path(infilepath).with_suffix(".svg")
    with open(outfilepath, "w") as outfile:
        read(infilepath).svg().write(outfile, indent=max(0, indent))


def validate_scale(ctx, param, value):
    if value <= 0.0:
        raise click.BadParameter("scale must be larger than 0.0")
    return value


@cli.command()
@click.option("-s", "--scale", default=1.0, type=float, callback=validate_scale)
@click.argument("infilepath", nargs=1, required=True)
@click.argument("outfilepath", nargs=1, required=False)
def png(scale, infilepath, outfilepath=None):
    "Convert NeoChart YAML to PNG file."
    write_png(scale, infilepath, outfilepath)


def write_png(infilepath, outfilepath=None, scale=1.0):
    if not outfilepath:
        outfilepath = pathlib.Path(infilepath).with_suffix(".png")
    inputfile = io.StringIO(repr(read(infilepath).svg()))
    with open(outfilepath, "wb") as outfile:
        outfile.write(cairosvg.svg2png(file_obj=inputfile, scale=scale))


if __name__ == "__main__":
    cli()
