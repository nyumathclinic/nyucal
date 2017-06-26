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


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


@pytest.fixture
def html_file(request):
    """NYU Academic Calendar HTML file"""

    path = 'New York University - University Registrar - Calendars - Academic Calendar.html'  # noqa
    f = open(os.path.join('golden', path))

    def teardown():
        f.close()

    request.addfinalizer(teardown)
    return f


@pytest.fixture
def calendar_store(request):
    return nyucal.CalendarStore(html_file(request))


def test_calendar_store_construction(html_file):
    store = nyucal.CalendarStore(html_file)
    assert isinstance(store, nyucal.CalendarStore)


def test_get_calendar_names(calendar_store):
    """Test the `CalendarStore.calendar_names (property)` method"""
    calendar_names = calendar_store.calendar_names
    gold_names = ['Fall 2016', 'Fall 2017', 'Fall 2018',
                  'January Term 2017', 'January Term 2018',
                  'Spring 2017', 'Spring 2018',
                  'Summer 2017', 'Summer 2018']
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


def test_write_csv(calendar_store, tmpdir):
    """Test writing to a CSV file"""
    calendar = calendar_store.calendar('Fall 2017')
    test_path = tmpdir.join('test.csv')
    with test_path.open('w') as test_file:
        writer = nyucal.GcalCsvWriter(test_file)
        writer.write(calendar)
    from difflib import unified_diff
    gold_path = os.path.join('golden', 'Fall2017.csv')
    with open(gold_path) as gold_file:
        lines = unified_diff(gold_file.readlines(), test_path.readlines(),
                             fromfile='expected', tofile='received')
        assert ''.join(lines) == ''


def test_command_line_interface():
    """Test the CLI. (boilerplate)"""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'nyucal.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
