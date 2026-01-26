***************
Release History
***************

.. currentmodule:: nasdaq_100_ticker_history

.. towncrier release notes start

Nasdaq_100_Ticker_History 2026.2.0 (2026-01-25)
===============================================

User-Visible Changes
--------------------
- Added Walmart (WMT) to the index, replacing AstraZeneca (AZN) effective January 20, 2026.
- Corrected the short-term addition and removal of Versant (VSNT) in early January 2026.
- Fixed the historical removal date for Solstice Advanced Materials (SOLS) to November 6, 2025.

Nasdaq_100_Ticker_History 2026.0.0 (2025-12-21)
===============================================

User-Visible Changes
--------------------
- On December 22, 2025, the annual NASDAQ-100 index reconstitution became effective. Six companies were removed (BIIB, CDW, GFS, LULU, ON, TTD) and six companies were added (ALNY, FER, INSM, MPWR, STX, WDC).

Internal Changes
----------------
- Update python dependencies.


Nasdaq_100_Ticker_History 2025.9.0 (2025-11-15)
===============================================

User-Visible Changes
--------------------
- On Oct 30, HON spun off SOLS, which was added to the n100 index.

Internal Changes
----------------
- Various internal improvements, including updating dependencies, improving type checking, and refactoring for clarity.


Nasdaq_100_Ticker_History 2025.8.0 (2025-10-10)
===============================================

Internal Changes
----------------
- Move to uv-build and src layout for the project
- Update python dependencies


Features
--------

- Thompson Reuters TRI replaces Ansys ANSS after Ansys was acquired by Synopsys.


Nasdaq_100_Ticker_History 2025.7.0 (2025-07-31)
===============================================

Features
--------

- Thompson Reuters TRI replaces Ansys ANSS after Ansys was acquired by Synopsys.


Nasdaq_100_Ticker_History 2025.6.0 (2025-07-06)
===============================================

Features
--------

- Add support for calendar year 2015.


Nasdaq_100_Ticker_History 2025.5.0 (2025-07-05)
===============================================

Internal Changes
----------------

- Refactor tests into per-year files for better organization.
- Add a GitHub workflow to validate pull requests.
- Update python dependencies.

Bug Fixes
---------

- Correctly handle the ticker symbol rename of Trip.com (formerly CTRP) in 2019.


Nasdaq_100_Ticker_History 2025.4.0 (2025-05-19)
===============================================

Features
--------

Update Nasdaq 100 constituents:
  - Shopify (SHOP) replaced MongoDB (MDB) on 19 May.


Nasdaq_100_Ticker_History 2025.2.0 (2024-12-25)
===============================================

Features
--------

Update dependencies for two moderate severity Jinja CVEs: CVE-2024-56201, CVE-2024-56326.


Nasdaq_100_Ticker_History 2025.1.0 (2024-12-15)
===============================================

Bug Fix
-------

The ticker symbol for Rivian Automotive Inc was incorrectly listed as RVIN instead of the correct RIVN during the period in 2022 - 2023 when it was in the index.  Thanks to DRAirey1 for catching this.


Nasdaq_100_Ticker_History 2025.0.0 (2024-12-14)
==============================================

Features
--------

Apply the annual `Nasdaq 100 index changes for 2024. <https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2024>`_

On December 13, as part of the annual reconstitution of the index, Nasdaq announced that three new companies would join the index prior to the market open on December 23, 2024. They are Palantir Technologies, MicroStrategy and Axon Enterprise. They will replace Illumina, Moderna, and Supermicro.


Nasdaq_100_Ticker_History 2024.5.0 (2024-07-28)
==============================================

Features
--------

Update Nasdaq 100 constituents:
  - Super Micro Computer Inc. (Nasdaq: SMCI) replaced Walgreens Boots Alliance Inc. (Nasdaq: WBA) on 22 July.


Nasdaq_100_Ticker_History 2024.3.0 (2024-06-24)
==============================================

Features
--------

Update Nasdaq 100 constituents:
  - ARM Holdings (ARM) replaced Sirius XM Radio (SIRI) on 24 June.


Nasdaq_100_Ticker_History 2024.2.1 (2024-04-16)
==============================================

Features
--------

Update dependencies for IDNA CVE-2024-3651
By side effect, this publishes the mypy type checking work as well.


Nasdaq_100_Ticker_History 2024.2.0 (2024-03-27)
==============================================

Features
--------

Add Mar index update:
  - Linde PLC replaces Splunk after Cisco completed the Splunk acquisition.


Nasdaq_100_Ticker_History 2024.1.0 (2024-02-29)
==============================================

Features
--------

Replace the problematic PyYaml with strictyaml.  No functionality change, just replacing a library that has caused build issues for many.


Nasdaq_100_Ticker_History 2024.0.0 (2023-12-26)
==============================================

Features
--------

Apply the annual `Nasdaq 100 index changes for 2023. <https://en.wikipedia.org/wiki/Nasdaq-100#Changes_in_2023>`_

There were two distinct changes:

  - On Dec 14, SeaGen (SGEN) was dropped after its merger with Pfizer, it was replaced by Take-Two Interactive (TTWO).

  - On Dec 18, the annual re-ranking was applied:
    - CDW, Coca-Cola Europacific Partners (CCEP), DoorDash (DASH), MongoDB Inc (MDB), Roper Technologies (ROP) and Splunk (SPLK) were added.
    - Align Technology Inc (ALGN), eBay (EBAY), Enphase Energy (ENPH), JD.com (JD), Lucid Group (LCID) and Zoom Video Communications (ZOOM) were dropped.

Update python dependencies for a Github-rated medium risk vulnerability in the urllib3 library.  `Reference <https://github.com/advisories/GHSA-g4mx-q9vg-27p4>`_

Nasdaq_100_Ticker_History 2023.3.0 (2023-10-03)
==============================================

Features
--------

Update python dependencies for a Github-rated medium risk vulnerability in the urllib3 library. `Reference <https://github.com/advisories/GHSA-v845-jxx5-vc9f>`_

Nasdaq_100_Ticker_History 2023.2.0 (2023-08-01)
==============================================

Features
--------

Add June and July Nasdaq changes:
  - On June 7, GE HealthCare Technologies replaced Fiserv.
  - On June 20, Onsemi replaced Rivian.
  - On July 17, The Trade Desk replaced Activision Blizzard.

Update python dependencies for a Github-rated low risk vulnerability in the certifi library.  CVE-2023-37920.


Nasdaq_100_Ticker_History 2023.1.0 (2023-06-01)
==============================================

Features
--------

Update python dependencies for a Github-rated medium risk vulnerability in the requests library.  `Reference <https://nvd.nist.gov/vuln/detail/CVE-2023-32681>`_


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
