import click

from .validators import regex_valid
from .topsis import topsis

@click.command()
@click.argument('input_file', nargs=1, type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument('weights', nargs=1, callback=regex_valid(r'^(\d+,)*\d+$'))
@click.argument('impacts', nargs=1, callback=regex_valid(r'^([+-],)*[+-]$'))
@click.argument('output_file', nargs=1, type=click.Path(dir_okay=False, writable=True))
def cli(input_file, weights, impacts, output_file):
    try:
        topsis(input_file, weights, impacts, output_file)
    except Exception as e:
        print(e)
