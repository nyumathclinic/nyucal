# -*- coding: utf-8 -*-

"""Console script for nyucal.

See click documentation at http://click.pocoo.org/

Auto-generated documentation coming soon.
See the sphinx-click_ plugin.

.. _sphinx-click: https://github.com/click-contrib/sphinx-click
"""

import click

from nyucal import nyucal


@click.group()
def main(args=None):
    """Console script for nyucal."""
    pass


@main.command()
@click.option('--source', '-s', default=nyucal.SOURCE_URL,
              help="""Calendars source (URL, file path, or string).
              (default: {} """.format(nyucal.SOURCE_URL))
def list(source):
    """List the available calendars in the calendar source

    Since the calendar store is, by default, scraped from a web page,
    this command will fail if no source is specified and the computer
    is not online.
    """
    store = nyucal.CalendarStore(source)
    for line in store.calendar_names:
        click.echo(line)


@main.command()
@click.argument('name', nargs=1)
@click.option('--source', '-s', default=nyucal.SOURCE_URL,
              help="""Calendars source (URL, file path, or string).
              (default: {} """.format(nyucal.SOURCE_URL))
@click.option('--format', '-f',
              type=click.Choice(['gcalcsv']),
              default='gcalcsv',
              help='Write in this format')
@click.option('--output', '-o', type=click.File('w'), default='-',
              help='Write to this file (default: stdout)')
def get(source, name, format, output):
    """Get the calendar named NAME and output in the specified format

    If NAME contains a space, it will need to be quoted.

    Since the calendar store is, by default, scraped from a web page,
    this command will fail if no source is specified and the computer
    is not online.
    """
    store = nyucal.CalendarStore(source)
    calendar = store.calendar(name)
    writers = {'gcalcsv': nyucal.GcalCsvWriter}
    writer = writers[format.lower()](output)
    writer.write(calendar)


if __name__ == "__main__":
    main()
