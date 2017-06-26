# -*- coding: utf-8 -*-

"""Console script for nyucal."""

import io

import click
from lxml import html
from nyucal import nyucal
import requests


@click.group()
def main(args=None):
    """Console script for nyucal."""
    click.echo("Replace this message by putting your code into "
               "nyucal.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


@main.command()
def list(source=None):
    if source is None:
        source = "https://www.nyu.edu/registrar/calendars/university-academic-calendar.html?display=2"  # noqa
    text = requests.get(source).text
    try:
        store = nyucal.CalendarStore(io.StringIO(text))
        for line in store.calendar_names:
            click.echo(line)
    except OSError:
        # text is such a big string that python's stack trace was flooded out by 
        # emitting the string.  So I checked on the exception's class name to find the
        # error type.  Then I guessed.
        click.echo("Something is wrong")


if __name__ == "__main__":
    main()
