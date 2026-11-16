# Nasdaq's index data endpoint is the authority for membership

Membership on a trading day is the start-of-day list that Nasdaq's index data endpoint (`indexes.nasdaqomx.com/Index/WeightingData`, `id=NDX`) returned for that day, as kept in the `ndx_ticker_history` database (mcc-invest/ndx-ticker-fetch).  Nasdaq's announcements confirm a change where one can be found; a change the endpoint shows that no announcement confirms still ships, marked as confirmed by the endpoint only.  The endpoint is Nasdaq's own day-by-day record of the index, and it reaches back to 2003-01-02, before this package's coverage began.

This replaces the ranking of sources in [ADR 0002](0002-membership-dates-follow-nasdaq-index-effective-date.md), which put announcements first.  Its rule that a change takes effect on the index effective date stands: the endpoint's start-of-day list for that date is where the change first shows.

## Considered Options

- **Announcements first, the endpoint only a pointer**, as ADR 0002 was written.  Rejected: the endpoint covers every trading day, while announcements from the early years survive only in archives, so a change whose release has been lost could never be recorded.
- **A change no announcement confirms blocks its year's release.**  Rejected for the same reason: the endpoint already answers the question the announcement would.

## Consequences

- A year file that disagrees with the endpoint is wrong.  Corrections ship as `fix:` commits, as under ADR 0002.
- The start-of-day list is the record.  The end-of-day list is a cross-check only, and a disagreement between them is resolved by hand, never silently.
- A member the endpoint marks `$X$` (stopped trading, not yet removed) stays a member under its last real symbol.
- Each change in a year file built from the endpoint names its confirming announcement, or says it is confirmed by the endpoint only.
- The package never reads the database.  Year files stay static YAML, drafted from the database and reviewed by hand.
- Years not yet checked against the endpoint keep the dates their announcements gave until they are.
