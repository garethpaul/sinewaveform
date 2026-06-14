# Make Root Override Protection

## Status: Completed

## Context

The Makefile derives repository paths from its own location, but command-line
and environment assignments can currently replace `ROOT`. A hostile or stale
caller-provided value can redirect package checks and builds away from the
checked-out source while still invoking the repository Makefile.

## Priority

Verification paths are a trust boundary. The repository must select its own
root while continuing to allow intentional `PYTHON`, `RUBY`, and `XCODEBUILD`
tool overrides.

## Objectives

- Make the repository-derived `ROOT` authoritative over environment and
  command-line assignments.
- Preserve the existing declaration position and all tool overrides.
- Verify package, waveform, podspec, and build paths from the repository and
  from an external working directory with hostile `ROOT` values.
- Add mutation-sensitive source, documentation, and completed-plan contracts.
- Keep hosted iOS Simulator compilation required on the exact pull-request
  head.

## Work Completed

- Marked the Makefile root assignment as an explicit GNU Make override.
- Extended the package checker to require exactly one protected declaration,
  preserved tool overrides, README indexing, and this plan's evidence.
- Kept application source, package metadata, the Xcode project, and workflow
  configuration unchanged.

## Verification

- `make check` passed through package, waveform, podspec, and static build
  checks; local `xcodebuild` was unavailable and used the documented static
  path.
- All five public Make aliases passed from both repository and external working
  directories with hostile environment and command-line `ROOT` assignments,
  for 20 bounded precedence cases.
- Package and waveform modes passed under Python 3.12 with networking disabled,
  a read-only source mount, and bytecode generation disabled.
- All three podspecs passed Ruby syntax checks, and checker compilation passed
  with its bytecode directed outside the repository.
- Seven declaration, duplicate, placement, alias, path, README, and plan
  mutations were rejected for the intended reason.
- Exact diff, protected-source, generated-artifact, high-confidence secret, and
  `git diff --check` audits passed. The pre-existing untracked checker bytecode
  remains excluded from the explicit-path commit.

Hosted macOS framework compilation remains required on the exact pull-request
head.

## Scope Boundary

This change does not alter waveform rendering, package metadata, the Xcode
project, workflow permissions, or dependency versions.
