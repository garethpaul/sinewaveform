# Bounded Waveform Drawing

## Problem

The waveform drawing code clamped unsafe wave counts and density values, but it
still drew with `0...waveCount`, producing one more wave than the configured
count. It also divided by view width and midpoint without first checking for a
valid graphics context and nonzero bounds, which can happen during preview or
layout transitions.

## TDD Evidence

1. Extended `scripts/check-sinewaveform-source.py --mode waveform` to reject the
   inclusive clamped wave loop and require graphics-context and bounds guards.
2. Updated `drawRect` to fetch the graphics context once, skip zero-size bounds,
   and iterate with `0..<waveCount`.
3. Kept the existing wave-count and density clamps in place for Interface
   Builder/runtime configuration safety.

## Verification

- `make lint`
- `make test`
- `make verify`
- `git diff --check`

`make build` runs the iOS simulator target when `xcodebuild` is installed;
otherwise it reports that static package checks completed.
