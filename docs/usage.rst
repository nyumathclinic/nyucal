=====
Usage
=====

Command line
============

To get the list of available calendars, use:

.. code-block:: console

    $ nyucal list

This will grab the latest version of the calendar from the NYU Registar's 
website.  You can also use a browser to save that webpage to a file on
your machine, and parse it offline with:

.. code-block:: console

    $ nyucal list *filename*

To get a specific calendar, use:

.. code-block:: console

    $ nyuget [-f/--format= format] [-o/--output= output_file] *name*

where *name* is one of the calendars named from :code:`nyucal list`.

You can save the output of :code:`nyucal get` to a file, either with the
:code:`>` shell operator or the :code:`-o/--output` option.  

The default format of the output is a CSV file that can be imported by 
Google Calendar.  In fact, this is the only format available at this time.
Future formats may include vCal.

GUI
===

Maybe someday.


Python library
==============    

To use :code:`nyucal` in a project::

    import nyucal

