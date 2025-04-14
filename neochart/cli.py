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
@click.argument("infilepath", nargs=1, required=True)
@click.argument("outfilepath", nargs=1, required=False)
def svg(infilepath, outfilepath=None):
    if not outfilepath:
        outfilepath = Path(infilepath).with_suffix(".svg")
    core.read(infilepath).write(outfilepath)


@cli.command()
@click.argument("infilepath", nargs=1, required=True)
@click.argument("outfilepath", nargs=1, required=False)
def png(infilepath, outfilepath=None):
    if not outfilepath:
        outfilepath = Path(infilepath).with_suffix(".png")
    buffer = io.StringIO(repr(core.read(infilepath).svg()))
    with open(outfilepath, "wb") as outfile:
        outfile.write(cairosvg.svg2png(file_obj=buffer))


if __name__ == "__main__":
    cli()
