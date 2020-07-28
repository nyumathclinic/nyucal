#!/usr/bin/env python

import io

from flask import Flask, render_template
from nyucal import nyucal


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/calendars')
def list_calendars():
    """List the available calendars in the calendar source

    Since the calendar store is, by default, scraped from a web page,
    this command will fail if no source is specified and the computer
    is not online.
    """
    store = nyucal.CalendarStore(nyucal.SOURCE_URL)
    return render_template('list.html', names=store.calendar_names)

@app.route('/calendar/<cal_filename>')
def get_calendar(cal_filename):
    """Get a calendar

    `cal_filename` includes an extension, which is used to determine
    the writer class.  The supported extensions are `.csv` and `.ics`.
    """
    cal_name, ext = cal_filename.split('.')
    store = nyucal.CalendarStore(nyucal.SOURCE_URL)
    calendar = store.calendar(cal_name)
    writers = {
        'csv': nyucal.GcalCsvWriter,
        'ics': nyucal.IcsWriter
    }
    mime_types = {
        'csv': 'text/csv',
        'ics': 'text/calendar'
    }
    output = io.StringIO()
    writer = writers[ext](output)
    writer.write(calendar)
    result = output.getvalue()
    output.close()
    response = app.make_response(result)
    response.mimetype = mime_types[ext]
    return response


