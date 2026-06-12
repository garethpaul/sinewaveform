# Changes

## 2026-06-12

- Rejected non-finite view dimensions before waveform geometry and sampling so
  invalid bounds cannot produce non-terminating draw work.
- Aligned the publishable root podspec with the hosted Swift 5 and iOS 12
  framework build while preserving archived release metadata.

## 2026-06-10

- Added a fixed macOS 15 CI job that builds the framework for a generic iOS
  Simulator and fixed portable checks to Ubuntu 24.04.
- Disabled persisted checkout credentials and made the two-job workflow an
  exact single-file repository contract.
- Updated the project to Swift 5 and iOS 12 and migrated the waveform view to
  current UIKit and Core Graphics APIs.
- Made Makefile verification and build paths independent of the caller's
  working directory.
- Bounded inspectable frequency, density, line widths, and phase shift through
  shared NaN-safe normalization before drawing.
- Preserved the declared idle-amplitude and phase-shift defaults when
  Interface Builder supplies NaN values.
- Added a least-privilege Python 3.12 GitHub Actions gate for portable checks.
- Clamped the final waveform sample to the right view edge so coarse density
  steps cannot produce off-bounds geometry or a negative edge envelope.

## 2026-06-09

- Centralized unit-interval normalization for level and idle-amplitude inputs
  so `NaN` values fall back before updating draw amplitude.
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
