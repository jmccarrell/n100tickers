# Bidirectional membership-changes API anchored at a fixed baseline date

## Context

The package's coverage of NASDAQ-100 membership history is expected to expand at both ends over time: forward as new changes are recorded each year, and backward as earlier history is uncovered. A new public API was needed for downstream consumers materializing the full history into a temporal data store.

## Decision

Expose the membership-changes stream as two iterators anchored at an invariant constant pair:

- `BASELINE_DATE: date` — fixed at `2020-01-01`.
- `BASELINE_MEMBERSHIP: frozenset[str]` — the hardcoded membership on that date, asserted equal to `tickers_as_of(2020, 1, 1)` by an invariant test.
- `changes_since() -> Iterator[MembershipChange]` — events with `effective_date > BASELINE_DATE`, in chronological order, forward-sense (additions/removals are what happened in real time).
- `changes_before() -> Iterator[MembershipChange]` — events with `effective_date <= BASELINE_DATE`, in **reverse chronological order** with **inverse-sense semantics**: each event's `additions` and `removals` describe what to apply when stepping *backward* through that date from the membership set you currently hold.

A consumer reconstructs membership at any covered date by folding the appropriate iterator onto `BASELINE_MEMBERSHIP`.

## Why this shape

The anchor is the load-bearing idea. With it, neither forward nor backward expansion shifts any previously-emitted event: forward expansion appends to `changes_since`, backward expansion appends to `changes_before`, and consumer rows from prior syncs remain valid. Expansion becomes pure-append on each side independently. `BASELINE_DATE = 2020-01-01` is roughly mid-coverage today, exercising both iterators end-to-end from day one.

## Considered and rejected: synthetic-baseline event

The obvious alternative was a single `changes()` iterator that emits the earliest Jan-1 baseline as a synthetic `MembershipChange(earliest, additions=initial_set, removals=frozenset())`, then real events. Rejected because backward expansion shifts the synthetic event's date *and* its tickers, breaking iterator idempotency: a row a consumer stored from a prior sync becomes wrong rather than just incomplete. The two-iterator anchor design preserves stable identity per emitted event under expansion in either direction.
