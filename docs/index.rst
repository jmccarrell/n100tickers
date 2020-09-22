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


nasdaq-100-ticker-history provides a historical view of the member companies of the NASDAQ 100
[#n100_overview]_.  As the members companies of this index change regularly [#n100_changes]_, the API
provides a date-centric view.  Ie, given a calendar date, it will return the set of ticker symbols (eg,
``AAPL``) that were in the index on that date.

As of version |version|, accurate coverage is provided for Jan 1, 2017 through Sep 22, 2020.

Example
-------

>>> from nasdaq_100_ticker_history import tickers_as_of
>>> 'AMZN' in tickers_as_of(2020, 6, 1)
True


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
