=======
changes
=======

.. currentmodule:: nasdaq_100_ticker_history

The membership-changes API exposes the NASDAQ-100 history as bidirectional
streams of additions and removals, anchored at a fixed baseline. See
``docs/adr/0001-bidirectional-membership-changes-api.md`` for the design
rationale.

.. autodata:: BASELINE_DATE

.. autodata:: BASELINE_MEMBERSHIP

.. autoclass:: MembershipChange
   :members:

.. autofunction:: changes_since

.. autofunction:: changes_before
