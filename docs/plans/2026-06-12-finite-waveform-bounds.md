# Finite Waveform Bounds

## Status: Completed

## Context

`SiriWaveformView.draw(_:)` rejects zero or negative bounds before dividing by
width and entering its sample loop. It does not reject non-finite dimensions.
An infinite width never satisfies the right-edge equality break while `x`
advances by a finite step, and non-finite dimensions can also feed invalid
coordinates into Core Graphics.

## Priority

Drawing must terminate and avoid Core Graphics operations whenever UIKit view
bounds are invalid, including non-finite dimensions.

## Requirements

- R1. Require finite width and height before clearing, filling, dividing, or
  sampling waveform geometry.
- R2. Preserve the existing positive-size guard and all normal finite drawing
  behavior.
- R3. Keep the right-edge clamp and bounded density step unchanged.
- R4. Add source contracts and focused mutations that reject removal of either
  finite-dimension check.
- R5. Update maintenance documentation and run the full `make check` gate.

## Scope Boundaries

- Do not change public inspectable properties, waveform shape, color, phase,
  amplitude, density, or packaging metadata.
- Do not add a new test target or alter the hosted workflow.
- Do not claim Interface Builder or device rendering without Apple tooling.

## Implementation Units

### Drawing boundary validation

**Files:** `SineWaveform/SineWaveForm.swift`

- Reject non-finite dimensions alongside non-positive bounds before graphics
  operations and waveform math.

### Regression contract and maintenance record

**Files:** `scripts/check-sinewaveform-source.py`, `README.md`, `SECURITY.md`,
`VISION.md`, `CHANGES.md`, `docs/plans/2026-06-12-finite-waveform-bounds.md`

- Require both finite dimension checks, preserve the existing size and
  right-edge contracts, and document the validation boundary.

## Verification Plan

- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- focused finite-bounds mutations
- `git diff --check`
- exact-head hosted iOS Simulator framework build before merge

## Work Completed

- Required finite, positive width and height before any graphics-context
  mutation, geometry division, or waveform sampling.
- Preserved the existing density normalization, right-edge clamp, and finite
  drawing behavior.
- Extended the checker and maintenance guidance for invalid UIKit geometry.

## Verification

- `python3 scripts/check-sinewaveform-source.py --mode waveform` passed.
- Four focused hostile bounds and ordering mutations were rejected.
- `make check` passed package and waveform checks; local `xcodebuild` was
  unavailable on Linux and the Makefile ran its documented static-only path.
- An external-directory repository Makefile invocation passed from `/tmp`.
- Root and archived podspec Ruby syntax, Python checker compilation, and
  `git diff --check` passed.
- Plan-aware correctness, maintainability, project-standards, testing,
  performance, reliability, and Swift lifecycle review found no actionable
  issues after a README wrapping fix.

## Remaining Risks

- Static contracts and compilation do not render the view in Interface Builder
  or exercise device graphics contexts.
