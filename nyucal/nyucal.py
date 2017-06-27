#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import print_function
import csv
from datetime import datetime
import inspect
import logging

from lxml import html


class CalendarStore(object):
    """Repository of academic calendars"""
    tree = None

    def __init__(self, flo=None):
        """Initializer"""
        if flo is not None:
            self.tree = html.parse(flo)

    @property
    def calendars(self):
        """The list of available calendars"""
        pass

    @property
    def calendar_names(self):
        """The list of available calendar names"""
        result = [elt.text.strip()
                  for elt in self.tree.xpath('//div[@class="calTitle"]')]
        return result

    def calendar(self, name):
        """Get a calendar by name."""
        log = logging.getLogger(inspect.currentframe().f_code.co_name)
        cal = Calendar()
        try:
            table = [
                elt.xpath('ancestor::table')[0]
                for elt in self.tree.xpath('//div[@class="calTitle"]')
                if elt.text.strip() == name
            ].pop()
        except:
            raise
        log.debug('table: %s', table)
        for row in table.findall('tbody/tr'):
            log.debug('row: %s', row)
            (event_date, event_end_date)\
                = self._parse_event_date_cell(row.find('td[1]'))
            (event_name, event_description)\
                = self._parse_event_text_cell(row.find('td[2]'))
            e = Event(start=event_date, end=event_end_date,
                      name=event_name, description=event_description)
            cal.add_event(e)
        return cal

    def _parse_event_date_cell(self, elt):
        """parse an event's date cell for the event's date
        (and end date too, if it exists)"""
        log = logging.getLogger(inspect.currentframe().f_code.co_name)
        fmt = '%A, %B %d, %Y'
        formatted_date = elt.text.rstrip(' -\xa0')
        log.debug('formatted_date: %s', formatted_date)
        event_date = datetime.strptime(formatted_date,
                                       fmt).date()
        log.debug('event_date: %s', event_date)
        # look for an end date, if it exists
        try:
            formatted_end_date = elt.find('br').tail
            log.debug('formatted_end_date: %s', formatted_end_date)
            event_end_date = datetime.strptime(formatted_end_date,
                                               fmt).date()
            log.debug('event_end_date: %s', event_end_date)
        except AttributeError:
            event_end_date = None
        return (event_date, event_end_date)

    def _parse_event_text_cell(self, elt):
        """Parse an event's text cell for the event's title
        (and description, if it exists)"""
        log = logging.getLogger(inspect.currentframe().f_code.co_name)
        # look for the event's title.  It shows up in several ways:
        # - inside a <strong> tag:
        event_name = elt.findtext('strong')
        event_desc = elt.text_content()
        # - if there's no text, inside the first b element:
        if (event_name is None and elt.text is None):
            event_name = elt.findtext('b')
        # - if there's a br tag, everything up to that tag (faulty)
        if (event_name is None and elt.find('br') is not None):
            event_name = elt.text
        # - if there's a :, everything up to it
        if (event_name is None and ':' in event_desc):
            (event_name, event_desc) = event_desc.split(':', 1)
        # - if there's a ., everything up to it
        if (event_name is None and '.' in event_desc):
            (event_name, event_desc) = event_desc.split('.', 1)
        # - last resort: entire text content
        if (event_name is None):
            event_name = event_desc
            event_desc = ""
        event_desc = event_desc.replace(event_name, "", 1).strip()
        log.debug('event_name: %s', event_name)
        log.debug('event_desc: %s', event_desc)
        return (event_name, event_desc)


class Calendar(object):
    """A single academic calendar"""
    name = None
    _events = None

    def __init__(self):
        self._events = []

    @property
    def events(self):
        """The list of available events in a calendar."""
        self._events = sorted(
                self._events,
                key=lambda d: (d.start, d.end, d.name))
        return self._events

    def add_event(self, event):
        """Add an event to the calendar."""
        self._events.append(event)


class Event(object):
    """A single event on an academic calendar"""

    name = None
    description = None
    start = None
    end = None

    def __init__(self, name=None, description=None, start=None, end=None):
        self.start = start
        self.end = end
        self.name = name
        self.description = description


class GcalCsvWriter(csv.DictWriter):
    """Class to write a Calendar to a CSV file suitable for importing to Google 
    Calendar.

    See `Google's documentation`_ on this CSV application.

    .. _`Google's documenation`: https://support.google.com/calendar/answer/37118?hl=en
    """  # noqa
    field_names = ['Subject', 'Start Date', 'End Date', 'All Day Event',
                   'Description']
    date_format = '%m/%d/%Y'

    def __init__(self, file):
        super(GcalCsvWriter, self).__init__(file, fieldnames=self.field_names)

    def write(self, calendar):
        """Write the calendar to the CSV file."""
        self.writeheader()
        for event in calendar.events:
            event_dict = {
                'Subject': event.name,
                'Start Date': event.start.strftime(self.date_format),
                'All Day Event': True,
                'Description': event.description
            }
            if event.end is None:
                event_dict['End Date'] = event_dict['Start Date']
            else:
                event_dict['End Date'] = event.end.strftime(self.date_format)
            self.writerow(event_dict)
