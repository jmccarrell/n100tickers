***************
Release History
***************

.. currentmodule:: nasdaq_100_ticker_history

.. towncrier release notes start

Nasdaq_100_Ticker_History 2023.0.0 (2022-12-19)
==============================================

Features
--------

On November 21, Enphase Energy replaced Okta.  `Reference <https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2022>`_

Update Nasdaq 100 index entries following the standard annual update, which takes effect on 2022-12-19.  `Reference <https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2022>`_

Update importlib.resources usage to follow the new interface.  `Reference <https://docs.python.org/3/library/importlib.resources.html#deprecated-functions>`_

Update python dependencies to address a moderate severity CVE in the certifi module.
`Reference <https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23491>`_


Nasdaq_100_Ticker_History 2022.3.0 (2022-06-09)
==============================================

Features
--------

Update python dependencies to address a moderate severity CVE in the py module.
`Reference <https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-42969>`_


Nasdaq_100_Ticker_History 2022.3.0 (2022-06-09)
==============================================

Features
--------

Meta Platforms, Inc. (Nasdaq: FB) today announced that its Class A common stock will begin trading on NASDAQ under the ticker symbol 'META' prior to market open on June 9, 2022.
`Reference <https://www.nasdaq.com/press-release/meta-platforms-inc.-to-change-ticker-symbol-to-meta-on-june-9-2022-05-31>`_


Nasdaq_100_Ticker_History 2022.2.0 (2022-02-21)
==============================================

Features
--------

- Excelon Corp (Nasdaq: EXC) announced it completed the separation of Constellation Energy Corp. (Nasdaq: CEG).  After review, Nasdaq has determined that Constellation Energy Corp. will remain as a component of the NASDAQ-100 Index®.  Thus CEG is added as of 2 Feb 2022.  `Reference <https://finance.yahoo.com/news/constellation-energy-corp-joined-nasdaq-010000704.html>`_

- Nasdaq (NDAQ) announced that AstraZeneca PLC - ADR (AZN), will become a component of the NASDAQ-100 Index (NDX) and the NASDAQ-100 Equal Weighted Index (NDXE) prior to market open on February 22, 2022. AstraZeneca PLC - ADR will replace Xilinx Inc. (XLNX) in the NASDAQ-100 Index® and the NASDAQ-100 Equal Weighted Index.  `Reference <https://www.nasdaq.com/articles/astrazeneca-to-join-nasdaq-100-index>`_
    - Advanced Micro Devices (AMD) is acquiring Xilinx in a transaction expected to be completed on or about February 14 2022.


Nasdaq_100_Ticker_History 2022.1.0 (2022-01-22)
==============================================

Features
--------

- Prior to market open on Monday, January 24, 2022. Old Dominion Freight Line, Inc. (Nasdaq: ODFL) will replace Peloton Interactive, Inc. (Nasdaq: PTON) in the NASDAQ-100 Index®.


Nasdaq_100_Ticker_History 2022.0.0 (2021-12-22)
============================================

Features
--------

- Provide support for the usual end-of-year Nasdaq 100 updates
    - Using as source data the wikipedia page: `Changes in 2021 <https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2021>`_
- Change the versioning scheme: the major version is the calendar year


Nasdaq_100_Ticker_History 0.5.0 (2021-10-02)
============================================

Features
--------

- Add support for calendar year 2016, using the `2016 data from the Wikipedia Nasdaq-100 page. <https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2016>`_


Nasdaq_100_Ticker_History 0.4.1 (2021-08-31)
============================================

Features
--------

- On August 26 2021, Crowdstrike replaced Maxim Integrated Products, who is being acquired by Analog Devices.  `Reference <https://en.wikipedia.org/wiki/Nasdaq-100#cite_ref-62>`_


Nasdaq_100_Ticker_History 0.4.0 (2021-07-31)
============================================

Features
--------

- Honeywell International Inc. to Join the NASDAQ-100 Index Beginning July 21, 2021.  `Reference <https://en.wikipedia.org/wiki/Nasdaq-100#cite_ref-61>`_


Nasdaq_100_Ticker_History 0.3.3 (2020-12-20)
============================================

Features
--------

- Add support for calendar year 2021.


Nasdaq_100_Ticker_History 0.3.2 (2020-12-19)
============================================

Features
--------

- Annual Changes to the Nasdaq-100 Index for 2020.  `2020 Annual Changes press release <https://www.nasdaq.com/press-release/annual-changes-to-the-nasdaq-100-index-2020-12-11>`_


Nasdaq_100_Ticker_History 0.3.1 (2020-11-27)
============================================

Features
--------

- Western Digital Corp (WDC) is replaced in the index by Keurig Dr Pepper Inc. (KDP) as of Oct 19, 2020.  `Oct 19 Changes press release <https://www.globenewswire.com/news-release/2020/10/10/2106521/0/en/Keurig-Dr-Pepper-Inc-to-Join-the-NASDAQ-100-Index-Beginning-October-19-2020.html>`_


Nasdaq_100_Ticker_History 0.3.0 (2020-09-23)
====================================================

Features
--------

- Renamed the module nasdaq_100_ticker_history.

- Removed function sorted_tickers_as_of.  It did not add much to the interface; better left to client code.


N100Tickers 0.2.2 (2020-09-17)
==============================

Features
--------

- Refactor the test code: DRY it up.
- Expand coverage to changes made to the Nasdaq 100 index components in 2017.
  The source of truth for these additions was wikipedia: `Nasdaq 100: Changes in 2017 <https://en.wikipedia.org/wiki/NASDAQ-100#Changes_in_2017>`_


N100Tickers 0.2.1 (2020-08-29)
==============================

Features
--------

- `Pinduoduo, Inc. to Join the NASDAQ-100 Index Beginning August 24, 2020 <https://www.globenewswire.com/news-release/2020/08/15/2078875/0/en/Pinduoduo-Inc-to-Join-the-NASDAQ-100-Index-Beginning-August-24-2020.html>`_


N100Tickers 0.2.0 (2020-08-23)
==============================

Features
--------

- Created docs for the project.
- Changed top-level function names.
