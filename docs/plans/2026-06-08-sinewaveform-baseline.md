# SineWaveform Baseline

## Status: Completed

## Context

`sinewaveform` is a legacy Swift `UIView` component for drawing a Siri-like
waveform and distributing it through CocoaPods metadata. The maintenance
baseline should keep package metadata and drawing loop safety checked even when
Xcode is unavailable.

## Objectives

- Preserve the `SiriWaveformView` public drawing surface and inspectables.
- Keep CocoaPods metadata syntax and source URLs valid.
- Validate waveform drawing guards for missing contexts, zero-size bounds,
  unsafe wave counts, and non-positive density values.
- Run package and waveform checks through `make check`.
- Maintain completed maintenance plans under `docs/plans`.

## Work Completed

- Confirmed `make check` runs podspec syntax, package metadata, waveform safety,
  and optional Xcode build checks.
- Added canonical `docs/plans` coverage for the current component baseline.
- Extended package checks to require completed `docs/plans` entries with
  `make check` verification.
- Updated README, VISION, and CHANGES to make the baseline discoverable.

## Verification

- `ruby -c SineWaveform.podspec`
- `python3 scripts/check-sinewaveform-source.py --mode package`
- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Run the iOS simulator target on macOS with Xcode installed.
- Add visual snapshot or sample-app verification before changing drawing output.
