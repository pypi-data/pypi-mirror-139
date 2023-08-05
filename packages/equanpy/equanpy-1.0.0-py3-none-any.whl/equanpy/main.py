import click
from equanpy.utils import hello


@click.command()
def cli():
    msg = hello()
    click.echo(msg)
