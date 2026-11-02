# Knope manages releases, and only user-visible changes cut one

Releases are cut by knope, a Rust tool, replacing Release Please.  A release follows a `feat:`, `fix:`, or breaking commit and nothing else: `docs:`, `deps:`, `ci:`, `refactor:`, `test:`, and `chore:` commits change no version and add no changelog entry.  This is the release behavior we want, not a cost of the switch: a new version of this package should mean its membership data or its behavior changed.

## Considered Options

- **Keep Release Please.**  Rejected: it runs on Node, and knope covers the same release PR, test gate, and draft-then-publish flow as a single Rust binary.
- **Make every Conventional Commit type cut a release, as Release Please does.**  Rejected: those releases shipped nothing a consumer could see.  knope cannot do it from squash titles anyway (knope-dev/knope#1727).

## Consequences

- A dependency change that reaches consumers, such as a new range in `pyproject.toml`, is titled `fix(deps):` so it is released.
- The changelog has only the sections knope fills from `feat:`, `fix:`, and breaking commits.  Entries are plainer: no compare link in the heading, and no "closes #N".
- The `2026.12.2` heading, the last Release Please wrote, is rewritten once into knope's format so that new entries land above it; the entries beneath it are untouched.
- The year rollover is forced by running the release workflow by hand with `--override-version`, since knope ignores `Release-As:` in commit bodies.
- `uv.lock` is bumped through a regex entry until knope supports it natively (knope-dev/knope#1995).
