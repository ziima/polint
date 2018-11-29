======
polint
======

.. image:: https://img.shields.io/pypi/v/polint.svg
    :target: https://pypi.org/project/polint/
    :alt: PyPI
.. image:: https://img.shields.io/pypi/l/polint.svg
    :target: https://pypi.org/project/polint/
    :alt: Licence
.. image:: https://img.shields.io/pypi/pyversions/polint.svg
    :target: https://pypi.org/project/polint/
    :alt: Python versions
.. image:: https://travis-ci.org/ziima/polint.svg?branch=master
    :target: https://travis-ci.org/ziima/polint
    :alt: Travis CI
.. image:: https://codecov.io/gh/ziima/polint/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ziima/polint
    :alt: Codecov

``polint`` is a linter for gettext PO files. It validates PO files against defined convensions.

-----
Usage
-----
::

    polint.py [options] <path>...
    polint.py -h | --help
    polint.py --version

To print complete usage use ``--help`` option.

------
Errors
------

* ``fuzzy`` - Translation is fuzzy
* ``obsolete`` - Entry is obsolete
* ``untranslated`` - Translation is missing. That includes ``fuzzy`` or ``obsolete``.
* ``location`` - Entry contains location data
* ``unsorted`` - Entry is not properly sorted
