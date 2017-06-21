# -*- coding: utf-8 -*-

"""Main module."""

class CalendarStore(object):
    """Repository of academic calendars"""

    def __init__(self, url=None):
        """Initializer"""
        pass

    @property
    def calendars(self):
        """The list of available calendars"""
        pass

class Calendar(object):
    """A single academic calendar"""
    name = None

    def __init__(self):
        pass

    @property
    def events(self):
        """The list of available events in a calendar."""
        pass

class Event(object):
    """A single event on an academic calendar"""

    date = None
    name = None
    description = None

    def __init__(self):
        pass

