# -*- coding: utf-8 -*-

"""Console script for nyucal.

See click documentation at http://click.pocoo.org/
"""

import io

import click

from nyucal import nyucal
import requests


@click.group()
def main(args=None):
    """Console script for nyucal."""
    click.echo("cli for nyucal")


@main.command()
def list(source=None):
    """List the available calendars in the calendar source"""
    if source is None:
        source = nyucal.SOURCE_URL  # noqa
    store = nyucal.CalendarStore(source)
    for line in store.calendar_names:
        click.echo(line)


if __name__ == "__main__":
    main()
