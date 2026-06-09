# Line Width Clamp

## Status: Completed

## Context

`SiriWaveformView` exposes primary and secondary line widths as inspectable
properties. Storyboard previews or runtime callers can set those values below
zero, and the draw loop previously passed them directly to Core Graphics.

## Objectives

- Preserve the public inspectable properties and normal drawing behavior.
- Clamp the draw-time line widths to nonnegative values before calling Core
  Graphics.
- Extend static waveform checks so the guard does not regress.

## Work Completed

- Added draw-time `primaryLineWidth` and `secondaryLineWidth` values clamped to
  `0.0` or higher.
- Updated `CGContextSetLineWidth` to use the clamped values.
- Extended `scripts/check-sinewaveform-source.py` to reject the raw line-width
  path and require the clamped drawing path.
- Documented the line-width guard in README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- `make verify`
- `git diff --check`

## Xcode Notes

`xcodebuild` was not available in this environment, so simulator build
verification was not run here. The repository `make check` wrapper still runs
`xcodebuild` when that tool is available locally.
