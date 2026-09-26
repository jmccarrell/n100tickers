We are going to publish a new version of this project.

Release Please owns the version bump, `CHANGELOG.md`, the tag, and the GitHub release: they follow from
the conventional-commit messages on `main`, and merging the release PR is what cuts the release.

The one thing it cannot do is refresh the coverage claim.  Before merging the release PR, update the end
date in @README.md in the phrase

accurate coverage is provided from Feb 1, 2007 through at least <date>

to the date through which coverage has been verified.
