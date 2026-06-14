# Exact Waveform Sample Budget

## Status: Planned

## Context

The width-derived sample step divides the view width by 4,096, but waveform
paths include both the zero and exact-right-edge samples. A budgeted path can
therefore contain 4,097 points, exceeding the declared per-wave sample budget.

## Priority

Medium rendering performance. The existing complexity guard should enforce its
stated point budget exactly while preserving endpoint geometry.

## Requirements

- Treat the sample budget as a point count including both endpoints.
- Derive the width step from `maximumSampleCount - 1` intervals.
- Preserve configured density when it produces fewer points.
- Preserve exact left- and right-edge samples, finite bounds, and wave limits.
- Add fail-closed source, documentation, and mutation contracts.

## Verification

- focused package and waveform source contracts
- repository and external-directory `make check`
- hostile point-budget, interval, step, endpoint, documentation, and plan mutations
- hosted iOS Simulator framework build on the exact pull-request head
- podspec syntax, generated-artifact, credential-pattern, and exact-diff audits
