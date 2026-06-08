# Waveform Package Gate

## Problem

The repository had no local verification command, root CocoaPods metadata used
legacy URL forms, and the waveform drawing loop could divide by zero or loop
without advancing if `numOfWaves` or `density` were set to unsafe values.

## TDD Evidence

1. Added `scripts/check-sinewaveform-source.py` and Makefile targets.
2. Ran `make lint` and confirmed package metadata failures for HTTPS/source URL
   expectations.
3. Ran `make test` and confirmed the waveform loop failed the clamping
   contracts.
4. Updated the podspec and drawing code, then reran the full verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `git diff --check`
