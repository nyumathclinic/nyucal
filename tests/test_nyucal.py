#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nyucal` package."""

import logging
import os.path
import sys

import pytest

from click.testing import CliRunner

from nyucal import nyucal
from nyucal import cli

from difflib import unified_diff
import py.path
import requests
from requests.exceptions import ConnectionError


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


@pytest.fixture
def goldendir(request):
    """Directory where golden files reside (a py.path.local object)
    """
    pwd = os.path.dirname(os.path.realpath(__file__))
    return py.path.local(os.path.join(pwd, 'golden'))


@pytest.fixture
def html_path(request, goldendir):
    """NYU Academic Calendar HTML file path"""
    path = 'New York University - University Registrar - Calendars - Academic Calendar.html'  # noqa
    return goldendir.join(path)


@pytest.fixture
def html_file(request, html_path):
    """NYU Academic Calendar HTML file object"""
    path = 'New York University - University Registrar - Calendars - Academic Calendar.html'  # noqa
    f = html_path.open()

    def teardown():
        f.close()

    request.addfinalizer(teardown)
    return f


@pytest.fixture
def html_string(request, html_file):
    """NYU Academic Calendar HTML as string"""
    return html_file.read()


gold_names = ['Fall 2016', 'Fall 2017', 'Fall 2018',
              'January Term 2017', 'January Term 2018',
              'Spring 2017', 'Spring 2018',
              'Summer 2017', 'Summer 2018']


@pytest.fixture
def calendar_store(request, html_file):
    return nyucal.CalendarStore(html_file)


def test_calendar_store_construction_from_file(html_file):
    store = nyucal.CalendarStore(html_file)
    assert isinstance(store, nyucal.CalendarStore)


def test_calendar_store_construction_from_string(html_string):
    store = nyucal.CalendarStore(html_string)
    assert isinstance(store, nyucal.CalendarStore)


def is_not_online():
    """check if the network is up"""
    try:
        requests.get('http://www.nyu.edu/')
        return False
    except ConnectionError:
        return True

onlyif_online = pytest.mark.skipif(
    is_not_online(),
    reason="Not online or nyu.edu is down",
)


@onlyif_online
def test_calendar_store_construction_from_url():
    store = nyucal.CalendarStore(nyucal.SOURCE_URL)
    assert isinstance(store, nyucal.CalendarStore)
    

def test_get_calendar_names(calendar_store):
    """Test the `CalendarStore.calendar_names (property)` method"""
    calendar_names = calendar_store.calendar_names
    assert len(calendar_names) == len(gold_names)
    for name in gold_names:
        assert name in calendar_names


def test_get_calendar(calendar_store):
    calendar = calendar_store.calendar('Fall 2017')
    assert isinstance(calendar, nyucal.Calendar)
    # generate the "golden" object.
    # import pickle
    # save_path = os.path.join('golden', 'calendar.pkl')
    # this should be in its own non-test method
    # with open(save_path, 'wb') as save_file:
    #     pickle.dump(calendar, save_file)
    # compare NOT WORKING.  Hard to compare
    # objects by attributes.
    # with open(save_path, 'rb') as save_file:
    #     golden_object = pickle.load(save_file)
    #     print(repr(calendar))
    #     print(repr(golden_object))
    #     assert calendar == golden_object


def test_write_csv(calendar_store, tmpdir, goldendir):
    """Test writing to a CSV file"""
    calendar = calendar_store.calendar('Fall 2017')
    test_path = tmpdir.join('test.csv')
    with test_path.open('w') as test_file:
        writer = nyucal.GcalCsvWriter(test_file)
        writer.write(calendar)
    gold_path = goldendir.join('Fall2017.csv')
    with gold_path.open() as gold_file:
        lines = unified_diff(gold_file.readlines(), test_path.readlines(),
                             fromfile='expected', tofile='received')
        assert ''.join(lines) == ''


@pytest.fixture
def cli_runner(request):
    """A command line runner for click applications"""
    return CliRunner()


def test_command_line_interface():
    """Test the CLI. (boilerplate)"""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    # assert 'nyucal.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


@onlyif_online
def test_cli_list_default(cli_runner):
    """Test the `nyucal list` command with no arguments"""
    result = cli_runner.invoke(cli.main, ['list'])
    assert result.exit_code == 0


@onlyif_online
def test_cli_list_from_url(cli_runner, html_path):
    """Test the `nyucal list` command from a URL"""
    result = cli_runner.invoke(cli.main,
                               ['list', '--source=' + nyucal.SOURCE_URL])
    assert result.exit_code == 0
    for name in gold_names:
        assert name in result.output


def test_cli_list_from_file(cli_runner, html_path):
    """Test the `nyucal list` command from a local file"""
    result = cli_runner.invoke(cli.main,
                               ['list', '--source=' + str(html_path)])
    assert result.exit_code == 0
    for name in gold_names:
        assert name in result.output


def test_cli_get(cli_runner, html_path, goldendir):
    """Test the `nyucal get` command from a local file, to stdout

    I wanted to do more sophisticated diffing from the golden file
    to the output, but :code:`result.output` is a single string, not a list
    of lines.  Since the description fields contain newlines, simply
    splitting on `\n` is not going to convert the output to a list
    properly.  So we join all the lines of the golden file and check if
    the strings are equal.
    """
    result = cli_runner.invoke(
        cli.main, ['get', 'Fall 2017',
                   '--source=' + str(html_path),
                   '--format=gcalcsv'])
    gold_path = goldendir.join('Fall2017.csv')
    with gold_path.open() as gold_file:
        expected_text = ''.join(gold_file.readlines())
        received_text = result.output
        assert expected_text == received_text


def test_cli_get_to_file(cli_runner, html_path, goldendir, tmpdir):
    """Test the `nyucal get` command from a local file, to a temporary file
    """
    gold_path = goldendir.join('Fall2017.csv')
    test_path = tmpdir.join('Fall2017.csv')
    result = cli_runner.invoke(
        cli.main, ['get', 'Fall 2017',
                   '--source=' + str(html_path),
                   '--output=' + str(test_path),
                   '--format=gcalcsv'])
    with gold_path.open() as gold_file:
        expected_text = gold_file.readlines()
        received_text = test_path.open().readlines()
        diff = unified_diff(expected_text, received_text,
                            fromfile='expected', tofile='received')
        assert ''.join(diff) == ''
