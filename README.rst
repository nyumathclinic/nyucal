================================
NYU Academic Calendar Processing
================================

.. ignore

        .. image:: https://img.shields.io/pypi/v/nyucal.svg
                :target: https://pypi.python.org/pypi/nyucal

        .. image:: https://img.shields.io/travis/leingang/nyucal.svg
                :target: https://travis-ci.org/leingang/nyucal

        .. image:: https://readthedocs.org/projects/nyucal/badge/?version=latest
                :target: https://nyucal.readthedocs.io/en/latest/?badge=latest
                :alt: Documentation Status

        .. image:: https://pyup.io/repos/github/leingang/nyucal/shield.svg
        :target: https://pyup.io/repos/github/leingang/nyucal/
        :alt: Updates

:code:`nyucal` is for parsing the `NYU Academic Calendar`_ web page into
machine readable calendar formats.

Each semester we read that page to find the dates of various holidays and
deadlines.  We wanted a nice way to import those events into calendar software
(e.g., Google Calendar, which can also be imported into Slack).

This is also a simple exercise in creating python packages, including testing
and documentation.  

Features
--------

* Command-line interface (CLI)
* Python package

Full documentation can be found at https://nyucal.readthedocs.io.

License
-------

MIT License.

Credits
-------

:code:`nyucal` is built on some great python packages, including:

* lxml_ for parsing HTML files (even bad ones) into XML element trees,
  as well as searching and traversing them.

* click_ for creating high-functioning command line applications

The package structure itself was created with Cookiecutter_ and 
the `audreyr/cookiecutter-pypackage`_ project template.

.. _lxml: https://lxml.de/
.. _click: https://click.pocoo.org/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _NYU Academic Calendar: https://www.nyu.edu/registrar/calendars/university-academic-calendar.html

