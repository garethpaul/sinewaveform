# Right-Edge Sample Clamp

## Status: Completed

## Context

The waveform loop advanced through `width + step` so it could reach the right
side when density did not divide the view width evenly. That final iteration
used an x coordinate beyond `bounds.width`, which made the parabolic envelope
negative and submitted off-bounds geometry for Core Graphics to clip.

## Work Completed

- Clamped each horizontal sample to the view width before envelope and phase
  calculations.
- Stopped the draw loop immediately after emitting the exact right-edge point.
- Extended the static waveform checker to reject the previous overshoot loop
  and require bounded coordinates throughout the final sample calculation.
- Documented the bounded drawing contract in the maintenance guidance.

## Verification

- `make check`
- Negative source mutation check restoring the prior overshoot loop
- `git diff --check`

The hosted macOS CI job provides the iOS Simulator framework build because
`xcodebuild` is not available in the Linux development environment.
