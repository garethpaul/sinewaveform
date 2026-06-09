# Waveform Amplitude Clamp

## Status: Completed

## Context

`SiriWaveformView.updateWithLevel` accepts caller-provided levels and combines
them with the inspectable `idleAmplitude`. The draw loop is now guarded against
bad counts, steps, and bounds, but amplitude values above the expected range can
still distort the waveform beyond the component's predictable drawing envelope.

## Objectives

- Keep the public `updateWithLevel(_:)` behavior and inspectable properties.
- Clamp caller-provided levels and `idleAmplitude` into the `0...1` drawing
  range before storing `_amplitude`.
- Add static verification for the bounded amplitude path.

## Work Completed

- Clamped `level` and `idleAmplitude` in `updateWithLevel`.
- Stored `_amplitude` from the clamped values rather than the raw caller input.
- Extended `scripts/check-sinewaveform-source.py` to reject the old unbounded
  assignment and require the clamped amplitude path.
- Documented the amplitude guard in README, VISION, and CHANGES.

## Verification

- `ruby -c SineWaveform.podspec`
- `python3 scripts/check-sinewaveform-source.py --mode package`
- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add a visual snapshot or sample-app verification path once an Xcode simulator
  environment is available.
- Document recommended caller level ranges in the public README examples.
