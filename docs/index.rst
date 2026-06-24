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

As of version |release|, accurate coverage is provided from Jan 1, 2015 through at least June 22, 2026.  Most
likely, the coverage is accurate further into 2026 subject to additional changes being announced by Nasdaq.  A new
version of the API is released on each update Nasdaq announces, typically with a time lag of a few days to a
few weeks.  It is the intent of the project maintainers to provide accurate coverage on an ongoing basis.

Examples
--------

Point-in-time membership via :func:`tickers_as_of`:

>>> from nasdaq_100_ticker_history import tickers_as_of
>>> 'AMZN' in tickers_as_of(2020, 6, 1)
True
>>> tuple(('OKTA' in tickers_as_of(y, 1, 1) for y in [2020, 2021, 2022, 2023]))
(False, True, True, False)

The membership-changes API exposes the index history as bidirectional streams
of additions and removals, anchored at a fixed ``BASELINE_DATE`` (January 1,
2020) so coverage expansion in either direction does not shift any previously
emitted event:

>>> from nasdaq_100_ticker_history.changes import (
       BASELINE_DATE, BASELINE_MEMBERSHIP, changes_since, changes_before,
    )
>>> first_post_baseline = next(iter(changes_since()))
>>> first_post_baseline.effective_date.isoformat()
'2020-04-20'
>>> 'DXCM' in first_post_baseline.additions
True
>>> 'AAL' in first_post_baseline.removals
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
