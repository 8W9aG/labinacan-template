# Semantic Versioning 2.0.0

**Citation.** Tom Preston-Werner. "Semantic Versioning 2.0.0". A specification, published at [semver.org](https://semver.org/spec/v2.0.0.html), with its source in [semver/semver](https://github.com/semver/semver). Licensed CC BY 3.0. No venue: it is a web specification, not a paper. The specification gives no date of its own. Version 2.0.0 dates from 2013.

**Status.** Used. `scripts/changelog.py next` proposes the release's version by its rules, and the `semantic-versioning` skill follows it.

**Read.** On 2026-11-26, the whole of `semver.md` in the source repository at commit `f99d548`, in the source's own text. That covers the summary, the introduction, the 11 numbered rules, the grammar, the reasons and the FAQ.

## Summary

**Claim.** Version numbers can say what changed from one release to the next. A project then declares a public API and follows a fixed set of rules.

**Method.** A version is `MAJOR.MINOR.PATCH`. The specification states its rules in the key words of RFC 2119.

**Findings, as the source states them.**

| Rule | Text |
| --- | --- |
| The public API | Software using Semantic Versioning "MUST declare a public API". |
| Major | It is incremented "if any backward incompatible changes are introduced to the public API". |
| Minor | It is incremented "if new, backward compatible functionality is introduced to the public API". |
| Patch | It is incremented "if only backward compatible bug fixes are introduced". |
| Version zero | "Major version zero (0.y.z) is for initial development. Anything MAY change at any time." |
| A released version | "the contents of that version MUST NOT be modified". |

## Where the claims go beyond the evidence

**It is a convention, not a measured result.** The specification argues from the problem of "dependency hell", and gives no study of projects that follow it.

**What counts as breaking is left to the project.** The rules turn on the public API, which each project declares for itself. Two projects can call the same change breaking or not.

## Use in this repo

**The release uses it.** The `release` skill runs the `semantic-versioning` skill before it bumps the version, and `scripts/changelog.py next` gives the version with its reasons.

**Version zero.** While the version is 0.y.z, the template bumps the minor number for a breaking change and the patch number for any other. The specification allows that: anything may change in initial development.

**The public API is declared per project.** Each project lists its breaking surfaces in the `semantic-versioning` skill's `project.md`, which answers the specification's first rule.
