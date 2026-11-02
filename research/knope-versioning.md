# Can knope version this package the way Release Please does?

Research for jmccarrell/n100tickers#121 (map: #120).

**Version checked:** knope 0.23.2 (released 2026-10-22, tag `knope/v0.23.2`,
commit `1fe8cde7fd36ac92451d307501f64f5d38dd30ac`), the latest release at the
time of writing. All doc citations are the knope.tech sources as they live in the
repo at that tag (`docs/src/content/docs/...`); all source citations are files
under `crates/` at that tag.

Base URL for citations below:
`https://github.com/knope-dev/knope/blob/knope/v0.23.2/`

## Summary

| Requirement | Verdict |
|---|---|
| CalVer `YYYY.minor.patch` + forced year rollover | Yes, with a workaround for the rollover |
| Bump rules from Conventional Commits | **No** for "every other type bumps patch"; yes for the rest |
| Bump `pyproject.toml` and `uv.lock` together | Yes, with a workaround for `uv.lock` (regex) |
| `v`-prefixed tags, continue from `v2026.12.1`, no manifest | Yes |

## 1. CalVer `YYYY.minor.patch` and the year rollover

**CalVer itself: yes.** knope only knows semver (`<major>.<minor>.<patch>`), and
`2026.12.1` is a valid semver with major `2026`. The bump rules are plain
increments: major resets minor and patch, minor resets patch
(`docs/.../reference/Concepts/semantic-versioning.md`;
`crates/knope-versioning/src/semver/rule.rs`). The special `0.x` handling does not
apply because the major is never `0`. So treating the year as the major works the
same way it does in Release Please today, including the same hazard: any breaking
change (`!` or a `BREAKING CHANGE:` footer) jumps the year.

**Year rollover: yes, with a workaround.** knope has no equivalent of the
`Release-As:` commit footer. It ignores commit bodies entirely and only reads
`BREAKING CHANGE`, `Changelog-Note` and configured custom footers
(`docs/.../reference/Concepts/conventional-commits.mdx`;
`crates/knope-versioning/src/changes/conventional_commit.rs`). Two ways to force
`2027.0.0`:

- `--override-version 2027.0.0` on the knope workflow that runs `PrepareRelease`
  (single-package syntax takes a bare version)
  (`docs/.../reference/command-line-arguments.md#--override-version`). In the source,
  an override bypasses the "nothing to release" check and is applied as
  `ChangeConfig::Force` (`crates/knope/src/step/releases/package.rs`,
  `crates/knope-versioning/src/package.rs::apply_changes`). In CI this means a
  `workflow_dispatch` input, or a one-off run, that passes the flag.
- A `feat!:` / `BREAKING CHANGE:` commit in January: from `2026.x.y` the major rule
  gives exactly `2027.0.0`. It works with no extra plumbing, but the changelog
  entry lands under "Breaking Changes", which mislabels it.

## 2. Bump rules from Conventional Commits

What matches today's behavior:

- `feat` -> minor, `fix` -> patch (`conventional_commit.rs`, `rule.rs`).
- `!` or a `BREAKING CHANGE` footer -> major, regardless of type.
- A subject that is not a Conventional Commit is ignored and moves nothing:
  `ConventionalCommit::parse(...)` failing returns no changes
  (`conventional_commit.rs::changes_from_commit_message`).

What does **not** match: **`docs`, `deps`, `ci`, `refactor`, `test`, `chore` do
not bump the version.** The commit-type mapping is hard-coded:

```rust
let commit_description_change_type = if commit.breaking() && !has_breaking_footer {
    ChangeType::Breaking
} else if commit.type_() == Type::FEAT {
    ChangeType::Feature
} else if commit.type_() == Type::FIX {
    ChangeType::Fix
} else {
    return changes; // The commit description isn't a change itself, only (maybe) footers were.
};
```

(`crates/knope-versioning/src/changes/conventional_commit.rs`.) The docs say the
same: "Knope ignores every other type, so they have no impact on the changelog or
versioning" (`conventional-commits.mdx`).

`extra_changelog_sections` does not help: its `types` are **changeset** types, not
commit types (`docs/.../recipes/customizing-release-notes.mdx`: "Each section
accepts any number of conventional commit footers and changeset types"). Only
footers are matched against sections in `conventional_commit.rs`. Custom footer
and custom changeset changes do bump patch (`rule.rs`:
`ChangeType::Custom(_) | ChangeType::Fix => Self::Patch`).

An open upstream issue asks for exactly this:
knope-dev/knope#1727 "Allow defining custom conventional commit types" (opened
2026-01-17, open, no maintainer reply), which quotes the same hard-coded block.

Workarounds, none clean:

- **Accept the change**: a release window with only `docs`/`ci`/... commits produces
  no release (set `allow_empty = true` on `PrepareRelease` so the workflow doesn't
  fail; `docs/.../reference/Config File/Steps/prepare-release.md`). Those commits
  also vanish from the changelog, so the "Documentation", "Dependencies" and
  "Internal Changes" sections go away.
- **Footers**: a `Changelog-Note:` or custom footer in the squash body bumps patch
  and adds a changelog entry. This moves the signal out of the squash title, which
  #120 says must stay the source.
- **Changeset files**: excluded by #120.
- **Script the bump**: a `Command` step / CI step that classifies commits since the
  last tag and passes `--override-version`. Reimplements the bump logic outside
  knope.
- Upstream a fix for #1727.

## 3. `pyproject.toml` and `uv.lock` together

**`pyproject.toml`: yes, native.** `versioned_files = ["pyproject.toml"]` updates
PEP 621 `[project] version` (`docs/.../reference/Config File/packages.mdx#pyprojecttoml`;
`crates/knope-versioning/src/versioned_file/pyproject.rs`). `dependency` is not
supported for it, which doesn't matter here.

**`uv.lock`: yes, with a regex workaround.** There is no `uv.lock` handler in
`crates/knope-versioning/src/versioned_file/`; knope-dev/knope#1995 "Feature
request: support `uv.lock`" (opened 2026-07-30) is open with no reply. knope's
generic regex file support covers it (`packages.mdx#regex-patterns`;
`versioned_file/regex_file.rs`):

```toml
[package]
versioned_files = [
    "pyproject.toml",
    { path = "uv.lock", regex = 'name = "nasdaq-100-ticker-history"\nversion = "(?<version>[^"]+)"' },
]
```

Behavior from `regex_file.rs`: the pattern must contain a named `version` group;
every pattern must match when reading, and the captured value must parse as a
version and equal the other files' versions; on write, `replace_all` rewrites the
`version` group inside each match. Against the current `uv.lock` this pattern
matches exactly once and captures `2026.12.1` (checked with an equivalent Python
regex; knope itself was not run). Like Release Please's `extra-files` JSONPath,
it only rewrites the line and does not re-run `uv lock`.

## 4. `v`-prefixed tags, continuing from `v2026.12.1`, no manifest

**Yes.** With the single `[package]` syntax, the `Release` step tags `v{version}`
(`docs/.../reference/Config File/Steps/release.md#tagging-format`;
`crates/knope-versioning/src/action.rs::ReleaseTag::tag_prefix` returns `"v"` when
the package has no custom name).

knope keeps no manifest. It derives the current version from the tags reachable
from `HEAD`: `all_tags_on_branch` walks `HEAD`'s history
(`crates/knope/src/integrations/git.rs`), and `PackageVersions::from_tags` takes
the newest `v`-prefixed tag that parses as a version
(`crates/knope-versioning/src/semver/package_versions.rs`). `PrepareRelease` then
reads every commit after that tag (`step/releases/conventional_commits.rs`,
`git.rs::get_commit_messages_after_tag`). `v2026.12.1` is on `2d7be39`, which is
on `main`, so knope picks up from it with no seeding.
`.release-please-manifest.json` can simply be deleted.

`Release` also decides whether there is something to release by comparing the
version in the files with the latest tag (`step/releases/mod.rs::find_prepared_release`),
so `pyproject.toml` at `2026.12.1` and the tag `v2026.12.1` must agree at
cutover. They do today.

## Blockers

- **CalVer: no blocker.** Rollover needs `--override-version` (or a mislabeled
  `feat!:`) instead of a `Release-As:` footer.
- **`uv.lock`: no blocker.** Regex entry in `versioned_files`.
- **The real gap is bump rules**: knope 0.23.2 cannot make `docs`/`deps`/`ci`/
  `refactor`/`test`/`chore` commits move the version or appear in the changelog.
  #120 must either accept that behavior change or pick one of the workarounds in
  section 2.
