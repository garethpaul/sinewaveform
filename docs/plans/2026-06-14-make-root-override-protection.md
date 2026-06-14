# Make Root Override Protection

## Status: Planned

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

## Planned Work

- Mark the Makefile root assignment as an explicit GNU Make override.
- Extend the package checker to require exactly one protected declaration and
  this plan's completed evidence.
- Exercise environment and command-line precedence through all public Make
  aliases without changing application or package source.

## Verification Plan

- Run package and waveform checks plus full `make check` from repository and
  external working directories.
- Run Ruby syntax checks for all podspecs and Python checker compilation.
- Reject weakened override, duplicate declaration, path, documentation, plan,
  and alias mutations.
- Audit the exact diff, generated artifacts, secrets, and protected source.
- Require the hosted macOS framework build on the exact pull-request head.

## Scope Boundary

This change does not alter waveform rendering, package metadata, the Xcode
project, workflow permissions, or dependency versions.
