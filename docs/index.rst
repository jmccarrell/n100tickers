.. nasdaq-100-ticker-history documentation master file, created by
   sphinx-quickstart on Sun Aug 23 12:22:32 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

nasdaq-100-ticker-history: Nasdaq 100 index company symbols over time
=====================================================================

.. toctree::
   :maxdepth: 1
   :hidden:

   changelog


``nasdaq-100-ticker-history`` provides the current set and a limited recent history of the stock symbols of
the member companies of the NASDAQ 100 [#n100_overview]_ index.  As the member companies of this index
change regularly [#n100_changes]_, the API is date-centric.  Ie, given a calendar date, it will return the
set of ticker symbols (eg, ``AAPL``) that were in the index on that date.

Coverage
--------

As of version |release|, accurate coverage is provided from Jan 1, 2016 through at least Oct 25, 2022.  Most
likely, the coverage is accurate further into 2022 subject to additional changes being announced by Nasdaq.  A new
version of the API is released on each update Nasdaq announces, typically with a time lag of a few days to a
few weeks.  It is the intent of the project maintainers to provide accurate coverage on an ongoing basis.

Examples
--------

>>> from nasdaq_100_ticker_history import tickers_as_of
>>> 'AMZN' in tickers_as_of(2020, 6, 1)
True
>>> tuple(('OKTA' in tickers_as_of(y, 1, 1) for y in [2020, 2021]))
(False, True)

API
---

.. toctree::
   :maxdepth: 1
   :glob:

   api/*


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. rubric:: Footnotes

.. [#n100_overview] `NASDAQ 100 overview <https://en.wikipedia.org/wiki/NASDAQ-100>`_
.. [#n100_changes] `NASDAQ 100 changes <https://en.wikipedia.org/wiki/NASDAQ-100#Yearly_changes>`_
