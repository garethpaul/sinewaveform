# Changes

## 2026-06-09

- Shifted negative `fmod` phase remainders into the nonnegative sine cycle and
  added static validation for normalized phase range correction.
- Wrapped waveform phase accumulation to a single sine cycle so long-running
  updates do not grow `_phase` without bound.
- Capped draw-time wave counts so excessive `numOfWaves` inspectable values do
  not create unbounded rendering work.
- Clamped inspectable waveform line widths at draw time before passing them to
  Core Graphics.
- Clamped draw-time maximum amplitude to a nonnegative value so very short
  bounds do not invert waveform rendering.
- Clamped `updateWithLevel` input levels and `idleAmplitude` into the expected
  `0...1` waveform drawing range.
- Extended waveform static checks to preserve bounded amplitude assignment.

## 2026-06-08

- Removed empty placeholder podspec descriptions and added static package
  validation for non-empty description metadata.
- Aligned archived versioned podspec URLs with the root HTTPS/lowercase package
  metadata and extended static package checks across all tracked podspecs.
- Added `make check` as the shared repository verification alias.
- Guarded `drawRect` against missing graphics contexts and zero-size bounds.
- Changed the wave loop to draw within the clamped wave count instead of one
  extra wave.
- Extended the waveform checker to protect context, bounds, and loop-count
  contracts.
- Added a Makefile verification gate for podspec syntax, package metadata, and
  waveform drawing safety.
- Updated root CocoaPods metadata URLs to HTTPS and matched the GitHub repo URL
  casing.
- Guarded waveform drawing against zero wave counts and non-positive density
  steps from Interface Builder/runtime configuration.
- Documented local verification steps.
- Added canonical `docs/plans` coverage and made package checks require
  completed plans.
