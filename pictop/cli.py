

from pictop.model.scan import Scanner

import click


@click.group()
def cli():
    pass


@click.command()
@click.argument('path', type=click.Path(exists=True))
def scan(path):
    scanner = Scanner()
    scanner.scan(path)


if __name__ == '__main__':
    cli()