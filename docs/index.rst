.. n100tickers documentation master file, created by
   sphinx-quickstart on Sun Aug 23 12:22:32 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

n100tickers: Nasdaq 100 ticker symbols over time
================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

n100tickers is a python3 library that provides a historical view of the member companies of the NASDAQ 100
[#n100_overview]_.  As the members companies of this index change regularly [#n100_changes]_, the API
provides a date-centric view.  Ie, given a calendar date, it will return the set of ticker symbols (eg,
``AAPL``) that were in the index on that date.

As of version |version|, coverage is provided for the years 2018 through 2020.

Example
-------

>>> 'AMZN' in tickers_as_of(2020, 6, 1)
True


API
---

.. toctree::
   :maxdepth: 1
   :glob:

   api/*


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. rubric:: Footnotes

.. [#n100_overview] `NASDAQ 100 overview <https://en.wikipedia.org/wiki/NASDAQ-100>`_
.. [#n100_changes] `NASDAQ 100 changes <https://en.wikipedia.org/wiki/NASDAQ-100#Yearly_changes>`_
