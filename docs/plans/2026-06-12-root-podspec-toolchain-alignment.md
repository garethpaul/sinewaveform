# Root Podspec Toolchain Alignment

## Status: Completed

## Context

The Xcode project and hosted build now target Swift 5 and iOS 12, while the
publishable root podspec still advertised iOS 8 and omitted its Swift language
version. CocoaPods consumers could therefore select a deployment contract that
the maintained project no longer builds or verifies.

The versioned podspecs under `SineWaveform/0.0.4` and `SineWaveform/0.0.6` are
historical release snapshots, so their metadata remains unchanged.

## Objectives

- Align the current root podspec with the hosted Xcode build contract.
- Declare the Swift language version consumed by CocoaPods.
- Preserve archived release metadata as historical evidence.
- Add deterministic package checks for both required declarations.

## Work Completed

- Raised the root podspec deployment target from iOS 8 to iOS 12.
- Declared Swift 5 in the root podspec.
- Extended package checks to require both values and reject the retired root
  iOS 8 declaration.
- Updated package compatibility documentation.

## Verification

- `ruby -c SineWaveform.podspec`
- `python3 scripts/check-sinewaveform-source.py --mode package`
- `make check`
- `make verify`
- `git diff --check`
