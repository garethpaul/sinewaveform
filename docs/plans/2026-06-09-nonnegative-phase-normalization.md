# Nonnegative Phase Normalization

## Status: Completed

## Context

The waveform now wraps `_phase` with `fmod`, but negative `phaseShift` values
can produce a negative remainder. Sine drawing still works with negative
phases, but storing a nonnegative `0...2π` phase keeps the bounded accumulator
contract consistent and easier to reason about.

## Objectives

- Preserve phase wrapping to a single sine cycle.
- Shift negative `fmod` remainders into the nonnegative cycle.
- Keep the phase normalization logic centralized.
- Add static checks for the corrected range behavior.

## Work Completed

- Updated `normalizedPhase(_:)` to store the `fmod` result before range
  correction.
- Added a nonnegative return path for negative wrapped phase values.
- Extended `scripts/check-sinewaveform-source.py` to reject direct negative
  `fmod` returns.
- Updated README, VISION, and CHANGES notes for nonnegative phase
  normalization.

## Verification

- `python3 scripts/check-sinewaveform-source.py --mode package`
- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make lint`
- `make check`
- `make verify`
- `git diff --check`

`xcodebuild` is not installed in this environment, so `make check` reports that
the Xcode build was not run after static verification passes.
