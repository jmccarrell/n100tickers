# Can knope write CHANGELOG.md with the current sections?

Research for jmccarrell/n100tickers#123, part of the map jmccarrell/n100tickers#120.

**Version checked:** knope 0.23.2 (released 2026-10-22, the latest release), tag
`knope/v0.23.2`, commit `1fe8cde7fd36ac92451d307501f64f5d38dd30ac`. Docs were read from
the `docs/` tree at that tag, which is the source of knope.tech. Source links below are
pinned to the tag.

`SRC` = `https://github.com/knope-dev/knope/blob/knope/v0.23.2`

## Short answer

Not as it stands. knope can name the `feat` and `fix` sections whatever we like, but only
`feat:`, `fix:` and `!` commit subjects ever become changes. `docs:`, `deps:`, `ci:`,
`refactor:`, `test:` and `chore:` produce no changelog entry and no version bump. And the
existing history's `## [2026.12.1](...)` headings are not something knope recognizes, so
its first release would be appended to the bottom of the file, not the top.

| Question | Verdict |
|---|---|
| Map types to User-Visible Changes, Fixes, Documentation, Dependencies, Internal Changes | Partly. `feat` and `fix` sections can be renamed. `docs`, `deps`, `ci`, `refactor` cannot be mapped by commit type at all. |
| Hide `test`/`chore` while still bumping | No. Every type other than `feat`/`fix` is ignored for both the changelog and the version. Hidden-but-bumping does not exist. |
| Add entries above existing history without touching it | No, not without a one-time edit. knope inserts before the first heading that parses as `## <semver> ...`; none of the current headings parse, so it appends at the end of the file. |
| Heading and line format | `## 2026.12.2 (2026-11-01)` / `### Fixes` / `- <summary>`. No compare link; per-line format is templatable but the heading is not. |

## 1. Mapping commit types to sections

Default sections ([SRC]/crates/knope-versioning/src/release_notes/config.rs, `Sections::defaults`):
Breaking Changes (`!` / `BREAKING CHANGE`), Features (`feat`), Fixes (`fix`), Notes
(`Changelog-Note` footer).

`extra_changelog_sections` adds or overrides sections. Each entry takes `name`, `footers`,
and `types` ([SRC]/docs/src/content/docs/reference/Config%20File/packages.mdx,
[SRC]/crates/knope-config/src/changelog_section.rs). The `types` are **changeset types**,
not commit types: the customizing recipe says each section accepts "conventional commit
footers and changeset types" ([SRC]/docs/src/content/docs/recipes/customizing-release-notes.md).
`minor` maps to Features and `patch` to Fixes (`From<changesets::ChangeType>` in
[SRC]/crates/knope-versioning/src/changes/mod.rs), so renaming works:

```toml
[package]
extra_changelog_sections = [
    { types = ["minor"], name = "User-Visible Changes" },
    { types = ["patch"], name = "Fixes" },
]
```

What does not work is a section fed by a commit type. The commit parser
(`changes_from_commit_message` in
[SRC]/crates/knope-versioning/src/changes/conventional_commit.rs) turns the subject line into
a change only when the commit is breaking, `feat`, or `fix`; any other type returns early with
only its footers ("The commit description isn't a change itself, only (maybe) footers
were."). The conventional-commits concept page says the same: "Knope ignores every other
type, so they have no impact on the changelog or versioning"
([SRC]/docs/src/content/docs/reference/Concepts/conventional-commits.mdx).

So Documentation, Dependencies and Internal Changes could only be filled by a commit
**footer** (for example `Changelog-Docs: ...` in the squash body) or by changeset files.
#120 rules out changeset files, and a footer means typing the entry twice in every PR.

Custom sections render after the built-in ones, and overridden built-ins render after
non-overridden ones, in config order (recipe, "Overriding built-in sections"). Overriding
all of them in the order wanted gives a stable order.

## 2. Hiding `test` and `chore` while still bumping

No. There is no `hidden` flag, and there is nothing to hide: `test:` and `chore:` (and
`docs:`, `deps:`, `ci:`, `refactor:`) do not move the version. Only footer-sourced custom
sections bump, at `patch` ("The semantic version impact of any custom changes is `patch`",
recipe).

The consequence is bigger than the changelog. Today every Conventional Commit type cuts a
release (CLAUDE.md, "Conventional Commits"). Under knope, a run of only `docs:`/`ci:`
commits is "nothing to release", and `PrepareRelease` fails unless `allow_empty = true`
([SRC]/docs/src/content/docs/reference/Config%20File/Steps/prepare-release.md, "Errors").
That is a versioning-behavior change for #120 to decide, not only a section-layout one.

## 3. Prepending above existing history

`Changelog::with_release` ([SRC]/crates/knope-versioning/src/release_notes/changelog.rs)
walks the file and inserts the new release before the **first line for which `parse_title`
succeeds**. If no line succeeds, it appends the release at the end of the file.

`parse_title` requires `#` or `##`, then a space, then a version as the very next token,
parsed by `Version::from_str` ([SRC]/crates/knope-versioning/src/semver/mod.rs) as exactly
three `.`-separated integers. Our headings look like:

```markdown
## [2026.12.1](https://github.com/jmccarrell/n100tickers/compare/v2026.12.0...v2026.12.1) (2026-10-13)
```

The second token is `[2026.12.1](https://...)`, whose first part `[2026` is not an integer,
so it fails. `# Changelog` and `### Fixes` fail too. Every line fails, so the first knope
release lands at the **bottom** of `CHANGELOG.md`. The recipe warns about exactly this:
existing headers in a different format require updating "the _latest_ version to Knope's
format" (recipe, "Changing the header level").

Workaround: a one-time edit of the single newest heading to
`## 2026.12.1 (2026-10-13)` (dropping its compare link), done in the cutover PR. knope never
rewrites the rest of the file. That touches one past heading, which #120 lists as out of
scope ("Rewriting past changelog entries"), so it needs a decision.

Header level is detected from the second `#`-line in the file
(`Changelog::new`), which here is a `##` line, so new releases would be `##` as today.
Version numbers like `2026.12.2` parse fine as semver.

## 4. Heading and line format side by side

Release Please today:

```markdown
## [2026.12.1](https://github.com/jmccarrell/n100tickers/compare/v2026.12.0...v2026.12.1) (2026-10-13)


### Fixes

* move the CTRX removal from 2015-07-29 to its 2015-07-24 effective date ([#117](https://github.com/jmccarrell/n100tickers/issues/117)) ([983b3a0](https://github.com/jmccarrell/n100tickers/commit/983b3a0c...)), closes [#112](https://github.com/jmccarrell/n100tickers/issues/112)
```

knope with default templates and the section overrides above:

```markdown
## 2026.12.2 (2026-11-01)

### Fixes

- move the CTRX removal from 2015-07-29 to its 2015-07-24 effective date (#117)
```

- The release heading is fixed at `{version} ({date})` with today's UTC date
  (`release_title` in [SRC]/crates/knope-versioning/src/release_notes/mod.rs). There is no
  compare link and no way to template one.
- Sections are `###`, one blank line around them (Release Please uses two before each
  section).
- The summary is everything after `type: ` on the subject line, so a GitHub squash title's
  `(#117)` stays as plain text. knope does not turn it into a link or add `closes #112`.
- Lines are templatable with `[release_notes] change_templates` (0.21.1+), using
  `$summary`, `$commit_hash` (short, 7 characters, per
  [SRC]/crates/knope/src/integrations/git.rs), `$commit_author_name`, and with `[github]`
  configured, `$pr_number` / `$pr_author_login` (0.23.0+, one GitHub API call per change)
  ([SRC]/docs/src/content/docs/reference/Config%20File/release-notes.mdx). A close
  approximation of the current lines:

  ```toml
  [release_notes]
  change_templates = [
      "* $summary ([$commit_hash](https://github.com/jmccarrell/n100tickers/commit/$commit_hash))",
  ]
  ```

  gives `* move the CTRX removal ... (#117) ([983b3a0](.../commit/983b3a0))`. The commit
  link uses the short hash; the `#117` stays unlinked and `closes #112` has no equivalent.

## What this means for #120

- `feat` / `fix` sections and line format: workable, with cosmetic differences.
- `docs`, `deps`, `ci`, `refactor` sections: not reachable from commit types. Dropping those
  sections, or requiring a footer in squash bodies, are the only options.
- Release cadence: non-`feat`/`fix` work stops cutting releases. Accept that, or find
  another trigger; whether `--override-version` with `allow_empty` can force one was not
  checked here.
- Existing history: needs a one-time rewrite of the newest heading, or knope appends at the
  bottom.

[SRC]: https://github.com/knope-dev/knope/blob/knope/v0.23.2
