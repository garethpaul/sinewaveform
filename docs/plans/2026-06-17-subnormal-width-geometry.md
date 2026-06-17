---
title: Keep Subnormal Waveform Widths Out of Core Graphics
type: fix
date: 2026-06-17
---

# Keep Subnormal Waveform Widths Out of Core Graphics

Status: In Progress

## Context

`draw(_:)` accepts every finite positive width, then computes `mid = width / 2`
and evaluates the envelope as `1 / mid * (sampleX - mid)`. A smallest-positive
`CGFloat` can underflow to a zero midpoint, while other tiny midpoints can make
the reciprocal overflow. Both cases can produce non-finite coordinates after
the existing finite-bounds guard and pass them to Core Graphics.

## Requirements

- R1. Reject a width whose midpoint underflows to zero before clearing, filling,
  or sampling the graphics context.
- R2. Compute the waveform envelope with direct normalized division instead of
  a separately overflowing reciprocal.
- R3. Exercise the shared envelope math with a tiny nonzero midpoint and require
  a finite result.
- R4. Preserve normal waveform shape, endpoint sampling, the exact 4,096-point
  budget, and all public inspectable behavior.
- R5. Add mutation-sensitive source and executable coverage for removed or late
  midpoint validation and restored reciprocal math.
- R6. Keep portable validation truthful and require the exact-head hosted iOS
  Simulator build for UIKit compilation evidence.

## Scope Boundaries

- Do not change public API, sampling density, amplitude, phase, colors, or
  packaging metadata.
- Do not weaken the existing finite-bounds, executable math, or hosted build
  gates.

## Implementation Units

### U1. Share overflow-safe envelope math

- **Goal:** Calculate the normalized waveform envelope without an intermediate
  reciprocal and prove tiny nonzero midpoints remain finite.
- **Files:** `SineWaveform/WaveformMath.swift`,
  `Tests/WaveformMathTests/main.swift`
- **Verification:** Executable Swift math harness plus hostile reciprocal-math
  mutation.

### U2. Reject midpoint underflow before drawing

- **Goal:** Derive and validate the horizontal midpoint before any graphics
  context mutation, then use the shared envelope helper in the sample loop.
- **Files:** `SineWaveform/SineWaveForm.swift`,
  `scripts/check-sinewaveform-source.py`
- **Verification:** Source mutations for removed guard, late guard, and restored
  inline reciprocal math.

### U3. Record the boundary

- **Goal:** Synchronize maintenance and security guidance with completed
  verification evidence.
- **Files:** `README.md`, `CHANGES.md`, `AGENTS.md`, `VISION.md`, `SECURITY.md`,
  `docs/plans/2026-06-17-subnormal-width-geometry.md`
- **Verification:** Repository and external-directory `make check`, mutation,
  generated-artifact, and credential-pattern audits.

## Verification

- Planned: executable Swift math tests where `swiftc` is available.
- Planned: focused source and hostile mutations.
- Planned: repository and external-directory `make check`.
- Planned: exact-head hosted iOS Simulator framework build.
