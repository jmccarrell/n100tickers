# Membership dates follow Nasdaq's index effective date

A membership change is recorded on the index effective date named in Nasdaq's own announcement, and Nasdaq's announcements outrank every other source.  So a security stays a member after it stops trading if Nasdaq's announcement keeps it in the index, and the index briefly holds fewer securities if Nasdaq removes one before its replacement joins.  The package describes Nasdaq's index, and Nasdaq's announcements are the record of that index.

## Considered Options

- **Delisting date.** Remove a security the day it stops trading.  Rejected: it describes what was tradable, not what was in the index, and it would contradict Nasdaq's own releases — DIRECTV stopped trading on 2015-07-24, but Nasdaq kept it in the index until BioMarin replaced it on 07-27.
- **Wikipedia's dates.** Rejected: checked against Nasdaq's releases, Wikipedia was wrong on several dates.

## Consequences

- The number of members varies.  Tests assert the count Nasdaq's announcements imply, including the brief periods after a removal with no same-day replacement.
- Zero-weight members are members and are recorded.
- A date found to disagree with this rule is a bug.  Corrections ship as `fix:` commits, each with a changelog entry.
