# Hosted iOS Build

Status: Completed

## Context

Portable checks protected package metadata and waveform safety contracts, but
GitHub Actions did not compile the framework. The project and its single Swift
source file also used language and framework APIs from the Swift 2 era.

## Changes

- Fixed portable verification to Ubuntu 24.04 and added concurrency cancellation.
- Added a bounded macOS 15 job that builds an unsigned generic iOS Simulator
  framework with pinned checkout actions.
- Updated the Xcode project to Swift 5 language mode and an iOS 12 deployment
  target.
- Migrated the waveform view to current UIKit and Core Graphics syntax while
  preserving its bounded input normalization and drawing math.
- Made Makefile paths independent of the caller's working directory and added
  static contracts for the hosted build.

## Verification

- `make check`
- `make -f /path/to/sinewaveform/Makefile check` from outside the repository
- Negative workflow mutation checks
- `git diff --check`
- GitHub Actions `contract` and `build` jobs
