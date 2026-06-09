# NaN-Safe Unit Normalization

## Status: Completed

## Context

`updateWithLevel(_:)` clamped caller-provided level values and `idleAmplitude`
into `0...1` with inline `min(max(...))` expressions. That handles ordinary
out-of-range inputs, but a `NaN` audio level can survive those expressions and
poison `_amplitude`, which then feeds the draw-time sine calculation.

## Objectives

- Preserve the public `updateWithLevel(_:)` API and normal clamping behavior.
- Centralize unit-interval normalization for waveform inputs.
- Fall back to zero for `NaN` values before updating draw amplitude.
- Add deterministic static checks for the shared normalization path.

## Work Completed

- Added `normalizedUnitValue(_:)` for `0...1` waveform input normalization.
- Routed caller-provided levels and `idleAmplitude` through the shared helper.
- Added a `NaN` fallback before applying the existing range clamp.
- Extended `scripts/check-sinewaveform-source.py --mode waveform` to require
  the shared normalization path and reject inline level clamping.
- Updated README, VISION, and CHANGES notes for the NaN-safe amplitude guard.

## Verification

- `ruby -c SineWaveform.podspec`
- `python3 scripts/check-sinewaveform-source.py --mode package`
- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make lint`
- `make check`
- `make verify`
- `git diff --check`

`xcodebuild` is not installed in this environment, so `make check` reports that
the Xcode build was not run after static verification passes.
