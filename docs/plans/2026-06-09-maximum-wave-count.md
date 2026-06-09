# Maximum Wave Count Guard

## Status: Completed

## Context

`SiriWaveformView.drawRect` already clamps `numOfWaves` to at least one before
drawing, but the value remained unbounded above. Because `numOfWaves` is an
Interface Builder/runtime inspectable, an accidentally huge value could make a
single draw pass perform excessive work.

## Objectives

- Preserve the public `numOfWaves` inspectable API.
- Keep the lower-bound guard for zero or negative values.
- Add a draw-time upper bound for wave count.
- Extend static waveform checks so the bounded draw loop remains in place.

## Work Completed

- Added `maximumWaveCount` to `SiriWaveformView`.
- Changed `drawRect` to clamp wave count into `1...maximumWaveCount`.
- Updated the waveform checker to reject a lower-only wave-count clamp.
- Updated README, VISION, and CHANGES.

## Verification

- Negative: `python3 scripts/check-sinewaveform-source.py --mode waveform`
  failed before the Swift fix because `numOfWaves` had no upper bound.
- `python3 scripts/check-sinewaveform-source.py --mode package`
- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- `make verify`
- `git diff --check`

## Xcode Notes

`xcodebuild` was not available in this environment, so simulator build
verification was not run here. The repository `make check` wrapper still runs
`xcodebuild` when that tool is available locally.
