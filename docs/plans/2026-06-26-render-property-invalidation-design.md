# Render Property Invalidation Design

Status: Completed

## Problem

`SiriWaveformView.draw(_:)` reads six public inspectable properties directly:
color, wave count, primary and secondary line widths, frequency, and density.
Changing any of them after the backing layer has rendered does not call
`setNeedsDisplay()`, so UIKit may continue presenting stale waveform pixels
until an unrelated level update or invalidation occurs.

## Options Considered

1. Require callers to invoke `setNeedsDisplay()`. This leaks an internal UIKit
   rendering responsibility through otherwise self-contained public properties.
2. Invalidate every inspectable property. `idleAmplitude` and `phaseShift` only
   affect the next `updateWithLevel(_:)`, so immediate redraw would not produce
   the newly configured behavior.
3. Add `didSet` invalidation only to the six properties read directly by
   `draw(_:)`. This keeps current level-update semantics and redraws exactly the
   values that can alter the current frame.

## Decision

Use option 3. Each live rendering property calls `setNeedsDisplay()` from its
observer. Preserve the public names, types, defaults, inspectability, and draw
normalization behavior.

## Verification

- Add a hosted UIKit test that clears the layer invalidation state, mutates each
  property, and requires `needsDisplay()` to become true.
- Add portable source and hostile-mutation contracts for all six observers.
- Run local portable verification and exact-head hosted UIKit/Xcode gates.
- Require `make check` before merge.
