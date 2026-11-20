# Nasdaq-100 membership history

Which securities were in the Nasdaq-100 index on any given day, as Nasdaq itself defined the index on that day.

## Language

**Member**:
A security Nasdaq counts as a component of the Nasdaq-100 on a given day, whatever its weight.
_Avoid_: Constituent, holding

**Zero-weight member**:
A member that Nasdaq included in the index with no weight, usually only briefly.  It is still a member.

**Membership change**:
A set of additions and removals that take effect together on one index effective date.
_Avoid_: Swap, rebalance (a rebalance changes weights, not membership)

**Index effective date**:
The day a membership change first applies, as named in Nasdaq's announcement — usually "prior to market open" on that day.  Not the announcement date, and not the day a removed security stopped trading.
_Avoid_: Change date, delisting date

**Ticker**:
The symbol a member traded under on the day in question.  A rename is a membership change on its effective date, so a query for a past day returns the symbol of that day.  A fifth letter Nasdaq adds to a symbol for a few weeks (a D or E, as in JAVAD) is not a rename: the base symbol is recorded throughout.
_Avoid_: Current symbol

**Primary source**:
The start-of-day list Nasdaq's index data endpoint returned for a day (ADR 0004).  Nasdaq's own announcement of a membership change confirms it; failing that, an exchange or SEC notice such as a delisting notice or an 8-K.  Secondary sources, Wikipedia included, only point to where a primary source might be.
