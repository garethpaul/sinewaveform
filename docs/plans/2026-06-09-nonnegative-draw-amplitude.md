# Nonnegative Draw Amplitude

## Status: Completed

## Context

`SiriWaveformView.drawRect` subtracts a fixed stroke margin from half the view
height to compute maximum wave amplitude. Very short bounds could make that
value negative, which inverts the wave calculation instead of rendering a
bounded zero-height waveform.

## Objectives

- Preserve existing waveform drawing for normal view sizes.
- Clamp draw-time maximum amplitude to a nonnegative value.
- Extend static waveform checks to protect short-bounds behavior.
- Avoid broader Swift or drawing API modernization in this focused pass.

## Work Completed

- Replaced the raw `halfHeight - 4.0` amplitude calculation with
  `max(halfHeight - 4.0, 0.0)`.
- Extended `scripts/check-sinewaveform-source.py` to reject negative
  max-amplitude drift.
- Updated README, VISION, and CHANGES notes for the drawing guard.

## Verification

- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- `make verify`
- `git diff --check`

## Xcode Notes

`xcodebuild` was not available in this environment, so simulator build
verification was not run here. The repository `make check` wrapper still runs
`xcodebuild` when that tool is available locally.
