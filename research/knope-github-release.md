# Can knope's GitHub release flow keep the release PR and draft-then-publish steps?

Research for #122 (map #120). Checked 2026-11-01 against:

- knope **0.23.2** (tag `knope/v0.23.2`, released 2026-10-22): docs under
  `docs/src/content/docs/` (the source of knope.tech) and Rust source under `crates/knope/src/`
- **knope-dev/action v2.1.2** (2026-02-13): `action.yml`, `entrypoint.sh`
- GitHub REST docs (Releases) and GitHub's immutable-releases docs

Links are pinned to `knope/v0.23.2` so they stay valid.

## Verdict

Go. Every guarantee holds with the knope **CLI** in Actions. Two things change.
First, knope does draft, upload and publish inside one step.
Second, the tag appears when GitHub publishes the release, not before.
Don't use the hosted **Knope Bot**: it authors the release PR as its own App, not
`mcc-lab-agent`.

## Per-bullet answers

### 1. A reviewable release PR before anything is tagged: yes

The "Preview releases with pull requests" recipe ([recipe][r-pr]) is a `prepare-release` workflow:
`git switch -c release` → `PrepareRelease` → `git commit` → `git push --force` → `CreatePullRequest`.
`PrepareRelease` updates versioned files and the changelog and **creates no tag**: "[`PrepareRelease`]
will update the package versions without creating a release tag" ([Release step][r-release]).
`CreatePullRequest` updates the open PR in place if one already exists for that head/base
([docs][r-cpr], [source][s-cpr]). That is the same "always one open release PR" model as Release Please.

The title is a template (`chore: prepare release $version`), so `chore: release $version` can stay.

### 2. The test suite gating the release: yes, by workflow structure

knope runs no tests itself. The gate is a `verify` job that the `knope release` job `needs:`, the same
as today. `Release` is no-op safe. It "will create releases for any packages whose current versions
don't match their latest release tag" ([Release step][r-release]; `find_prepared_release` in
[`step/releases/mod.rs`][s-mod]). So a red `verify` stops the release, and a later green run picks it up.

### 3. The `mcc-lab-agent` App installation token: yes

knope reads the token from `GITHUB_TOKEN`, with no prompt when it is set ([env vars][r-env], [github config][r-gh]).
The source sends it as a plain `Authorization: token …` / `Bearer …` header
([`create_release.rs`][s-cr], [`create_pull_request.rs`][s-cpr]). Nothing is PAT-specific, so a
`ghs_` installation token from `actions/create-github-app-token` works. The recipe uses
`secrets.PAT` in two places, and both become the App token:

- `actions/checkout` `token:`, so the `git push` of the `release` branch is an App push and fires
  `Validate` on the PR
- `GITHUB_TOKEN` for `knope prepare-release`, so the App is the PR author and Jeff can approve it

The App needs Contents and Pull requests write, the same as today.

### 4. Draft → attach wheel/sdist → publish: yes, built into `Release`

When a package sets `assets`, the `Release` step will "Create the release in draft mode", "Upload the
assets one at a time", then "Update the release to no longer be a draft"
([Release step][r-release]). The source does exactly that. It POSTs `/releases` with
`draft: assets.is_some()` and `target_commitish` = HEAD sha. It uploads each resolved asset, then PATCHes
`{"draft": false}`. Any upload failure aborts before the publish ("Release has been created but not
published!") ([`create_release.rs`][s-cr]). So the immutable-release order holds, provided
`uv build` runs **before** `knope release` in the same job:

```toml
[package]
assets = "dist/*"
```

Gotchas found in the source:

- **An empty glob still publishes.** With the glob form, zero matches resolve to an empty list. The
  release is still created as a draft and then published with no assets ([`resolve_assets`][s-cr]).
  Keep today's `ls dist/*.whl dist/*.tar.gz` guard before `knope release`, and the post-publish
  `gh release view … isDraft,assets` check after it. Or list the two files explicitly; a missing listed
  file is an error ([Release step][r-release], "Errors" item 4).
- **Retry after a partial failure is manual.** A failed upload leaves a draft with no tag. The docs
  list "The release already exists on the forge" as a failure. knope's own repo keeps a
  `workflow_dispatch` path that runs `gh release upload` + `gh release edit --draft=false` on the draft
  ([`add_release_assets.yml`][s-own], [draft-assets recipe][r-draft]). Plan the same fallback rather
  than rerunning `knope release`. Not tested here.
- knope publishes with no `make_latest`, so GitHub's default "latest" choice applies (same as today).

### 5. When the tag is created relative to the draft: when GitHub publishes it

With a `[github]` forge configured, `Release` makes **no local git tag**. It only calls the GitHub
API with `tag_name` + `target_commitish` ([`step/releases/mod.rs`][s-mod], where `create_tag` is reached
only when no forge is set; [`create_release.rs`][s-cr]). GitHub's docs say `target_commitish`
"determines where the Git tag is created from"
([REST: create a release][gh-rest]). This repo already found that a draft has no tag of its own
(the Releasing section of `CLAUDE.md`, the reason for `force-tag-creation`). So the tag
`v<version>` comes into being at the publish PATCH, pointing at the checked-out HEAD sha. At that
moment immutability locks it ("its associated Git tag is locked", [immutable releases][gh-imm]).

Consequences:

- The Release Please problem that `force-tag-creation` solved goes away. knope publishes in the same step,
  so no later run sees a tagless draft as "the previous release".
- The checkout in the release job must be the squash-merged commit on `main`. The cleanest trigger is
  the current one: `push` to `main`, branching on the head commit message (`chore: release`), where
  `GITHUB_SHA` is that commit. The recipe instead uses `pull_request: closed`. If kept, check out
  `github.event.pull_request.merge_commit_sha` explicitly. That is my recommendation, not a recipe step.
- `PrepareRelease` reads local tags to find the last version, so `fetch-depth: 0` is required (recipe step 1).

### 6. How knope is installed in CI, and whether it runs on Node: no Node

`knope-dev/action` is a **composite** action (`runs: using: "composite"`) with one `bash` step
([`action.yml`][a-yml]). `entrypoint.sh` uses the preinstalled `gh` CLI to
`gh release download <tag> --repo knope-dev/knope --pattern "*x86_64*linux*"`, untars it, and adds the
directory to `PATH` ([`entrypoint.sh`][a-sh]). The binary is knope's prebuilt Rust release
(`knope-x86_64-unknown-linux-musl.tgz` on `knope/v0.23.2`). Node is never involved; the only runtime is
bash plus `gh` (Go).

Notes:

- Pin both: `uses: knope-dev/action@v2.1.2` with `version: 0.23.2` (the recipe does this). With no
  version it picks whatever release is latest.
- The pattern is x86_64-only, so it fits `ubuntu-latest`. An arm runner would need a direct
  `gh release download` instead.
- The action does no checksum verification. Running `gh release download` directly (or `cargo binstall knope`,
  or `cargo install knope`, which builds from source; [installation][r-inst]) are the alternatives. None
  of them uses Node either.

## Not covered here

`pyproject.toml` + `uv.lock` versioned files, CalVer, and changelog section mapping belong to sibling
tickets on #120.

[r-pr]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/docs/src/content/docs/recipes/1-preview-releases-with-pull-requests.md
[r-draft]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/docs/src/content/docs/recipes/uploading-assets-to-draft-releases.md
[r-release]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/docs/src/content/docs/reference/Config%20File/Steps/release.md
[r-cpr]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/docs/src/content/docs/reference/Config%20File/Steps/create-pull-request.md
[r-env]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/docs/src/content/docs/reference/environment-variables.md
[r-gh]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/docs/src/content/docs/reference/Config%20File/github.md
[r-inst]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/docs/src/content/docs/installation.mdx
[s-cr]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/crates/knope/src/integrations/github/create_release.rs
[s-cpr]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/crates/knope/src/integrations/github/create_pull_request.rs
[s-mod]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/crates/knope/src/step/releases/mod.rs
[s-own]: https://github.com/knope-dev/knope/blob/knope/v0.23.2/.github/workflows/add_release_assets.yml
[a-yml]: https://github.com/knope-dev/action/blob/v2.1.2/action.yml
[a-sh]: https://github.com/knope-dev/action/blob/v2.1.2/entrypoint.sh
[gh-rest]: https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#create-a-release
[gh-imm]: https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/immutable-releases
