# Waveform Sample Budget

## Status: Completed

## Context

Finite bounds prevented non-terminating geometry, but a very wide finite view
still generated roughly one horizontal sample per point for every wave. An
extreme programmatic layout could therefore create excessive Core Graphics path
work even though all inputs were valid.

## Priority

Input validity and rendering complexity are separate boundaries. Waveform path
generation should have a reviewed work budget while preserving normal-density
output and the exact terminal sample at the right edge.

## Objectives

- Cap each waveform path at approximately 4,096 horizontal samples.
- Preserve configured density when it already produces fewer samples.
- Preserve the clamped exact-right-edge terminal sample.
- Keep wave count and finite input normalization unchanged.
- Add fail-closed source, documentation, and completed-plan contracts.

## Work Completed

- Added a `maximumSampleCount` drawing constant.
- Derived `sampleStep` from the greater of configured density and the width
  budget.
- Kept terminal sampling through `min(x, width)`.
- Extended package, waveform, and documentation contracts.

## Verification

- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check` locally and from outside the repository root
- focused budget, derived-step, loop-step, right-edge, documentation, and plan
  mutations
- podspec syntax, Python checker compilation, XML, secret, artifact, and
  `git diff --check` audits
- hosted iOS Simulator framework compilation; runtime rendering remains manual

Package and waveform checks plus full `make check` passed locally with the
documented static-only path because `xcodebuild` is unavailable. All six
budget, derived-step, loop-step, right-edge, documentation, and plan mutation
categories were rejected. The root and both archived podspecs passed Ruby
syntax checks; Python checker compilation, high-confidence secret screening,
and `git diff --check` also passed. Checker compilation created an untracked
`scripts/__pycache__` directory; it is excluded from the explicit-path commit
and preserved. Hosted iOS Simulator framework compilation remains required on
the exact PR head.

## Scope Boundary

This bounds path construction complexity but does not add snapshot tests,
measure frame time, or exercise Interface Builder and simulator animation.
