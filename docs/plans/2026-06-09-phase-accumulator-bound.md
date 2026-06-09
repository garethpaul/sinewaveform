# Phase Accumulator Bound

## Status: Completed

## Context

`SiriWaveformView.updateWithLevel(_:)` advanced `_phase` by adding
`phaseShift` on every update. Long-running animations could let that value grow
without bound, eventually reducing sine precision even though drawing only
needs the phase within one cycle.

## Objectives

- Preserve the existing `phaseShift` animation behavior.
- Keep stored phase bounded to one sine cycle.
- Centralize phase normalization so future changes do not reintroduce raw
  accumulation.
- Add static checks for the bounded phase path.

## Work Completed

- Added a `phaseCycle` constant for the `2π` wrapping interval.
- Replaced raw `_phase += phaseShift` with normalized phase assignment.
- Added `normalizedPhase(_:)` using `fmod` from Darwin.
- Extended `scripts/check-sinewaveform-source.py` to require phase wrapping.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-sinewaveform-source.py --mode package`
- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- `git diff --check`

`xcodebuild` is not installed in this environment, so `make check` reports that
the Xcode build was not run after static verification passes.

## Follow-Up Candidates

- Document supported Swift, iOS, and CocoaPods versions.
- Add a small sample or snapshot verification path for waveform rendering.
