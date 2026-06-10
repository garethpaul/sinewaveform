# Finite Inspectable Inputs and CI

## Status: Completed

## Context

Interface Builder can supply arbitrary floating-point values for waveform
frequency, density, line widths, and phase shift. NaN or infinite values could
reach phase math or Core Graphics even though amplitude was already guarded.
The repository also had no automated CI for its portable static checks.

## Work Completed

- Added one shared finite-range normalization path for inspectable floating
  point inputs.
- Bounded frequency, density, line widths, and phase shift before drawing or
  phase accumulation while preserving mirrored negative-frequency rendering.
- Used each inspectable property's existing default as the fallback for NaN.
- Extended the static waveform checker to protect each normalization contract.
- Added a least-privilege Python 3.12 GitHub Actions workflow using immutable
  Node 24 action references.

## Verification

- `make check`
- Negative source and workflow mutation checks
- `git diff --check`

`xcodebuild` is unavailable in the Linux environment, so the existing Makefile
continues to run an Xcode simulator build only when that tool is installed.
