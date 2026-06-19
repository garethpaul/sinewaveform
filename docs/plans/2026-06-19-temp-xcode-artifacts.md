---
title: Keep Xcode Build Artifacts in Temp
type: fix
date: 2026-06-19
---

# Keep Xcode Build Artifacts in Temp

Status: Completed

## Context

The repository `make build` target invoked `xcodebuild` without a DerivedData
override. Local verification could therefore write build artifacts to the
user-global Xcode DerivedData location, even when reviewers intentionally kept
the working tree and generated artifacts isolated.

Current Xcode also requires a scheme when `-derivedDataPath` is supplied, so the
build command needs to use the shared `SineWaveform` scheme instead of only the
target form.

## Requirements

- R1. Keep `make build` and `make check` Xcode DerivedData under `TMPDIR` by
  default.
- R2. Preserve caller overrides for `PYTHON`, `RUBY`, `SWIFTC`, `XCODEBUILD`,
  `TMPDIR`, and `XCODEBUILD_DERIVED_DATA_PATH`.
- R3. Keep the repository root protected from caller overrides.
- R4. Preserve the existing generic iOS Simulator build, code-signing override,
  static package checks, and executable Swift math test path.
- R5. Add mutation-sensitive source coverage for the temp DerivedData path and
  scheme invocation.

## Work Completed

- Added a default `XCODEBUILD_DERIVED_DATA_PATH` under `TMPDIR`.
- Switched `make build` to the `SineWaveform` scheme and passed
  `-derivedDataPath`.
- Extended the package checker to reject Makefile mutations that drop the temp
  artifact override, scheme invocation, or DerivedData flag.
- Updated README, change log, and agent maintenance guidance.

## Verification

- The new package source contract failed before the Makefile fix.
- `python3 scripts/check-sinewaveform-source.py --mode package` passed.
- `python3 scripts/check-sinewaveform-source.py --mode waveform` passed.
- `sh scripts/run-waveform-math-tests.sh` passed.
- Repository and external-directory `make check` passed.
- Local Xcode iOS Simulator build passed with DerivedData under temp.
- Hosted CodeQL and workflow status were checked before landing; exact-head
  hosted checks remain required after push.
