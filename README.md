# sinewaveform

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Device Preview

<!-- DEVICE-PREVIEW-IMAGE -->
![Device preview](docs/device-preview.svg)

## Overview

`garethpaul/sinewaveform` is an Apple platform application or Objective-C/Swift sample. Produce a "Siri" like waveform.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C/C++ headers (1), Swift (1).

## Repository Contents

- `README.md` - project overview and local usage notes
- `CHANGES.md` - maintenance history for package and waveform checks
- `Makefile` - local verification entry points
- `docs/plans` - completed maintenance plans for the current baseline
- `plans` - historical implementation notes
- `scripts` - static package and waveform validators
- `SECURITY.md` - security reporting and disclosure guidance
- `SineWaveform` - source or example code
- `SineWaveform.xcodeproj` - Xcode project file
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: SineWaveform
- Dependency and build manifests: SineWaveform.podspec
- Entry points or build surfaces: SineWaveform.xcodeproj
- Test-looking files: no obvious test files detected

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- Python 3 and Ruby for repository source checks

### Setup

```bash
git clone https://github.com/garethpaul/sinewaveform.git
cd sinewaveform
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `SineWaveform.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- For CocoaPods package checks, start from the root `SineWaveform.podspec`.

## Testing and Verification

- `make check` runs podspec syntax checks, static package metadata checks, and
  waveform drawing safety checks for context availability, nonzero bounds, wave
  count, and draw step handling. When `xcodebuild` is installed, the `build`
  target also builds the `SineWaveform` target for the iOS simulator.
- Static waveform checks also require caller-provided levels and idle amplitude
  values to be clamped into the expected `0...1` drawing range.
- Static waveform checks also require level and idle-amplitude normalization to
  reject `NaN` before updating the draw amplitude.
- Static waveform checks also require draw-time maximum amplitude to stay
  nonnegative for very short view bounds.
- Static waveform checks also require inspectable line widths to be clamped
  before they are passed to Core Graphics.
- Static waveform checks also require draw-time wave counts to be capped so
  excessive inspectable values cannot make a draw pass unbounded.
- Static waveform checks also require phase accumulation to be wrapped to a
  single sine cycle on each level update.
- Static waveform checks also require negative phase remainders to be shifted
  into the nonnegative cycle.
- Static package checks cover the root and archived versioned podspec metadata.
- Static package checks reject empty placeholder podspec descriptions before
  the real package description.
- Static package checks also require completed canonical plans under `docs/plans`.
- Xcode's test action or `xcodebuild test` with the appropriate scheme and
  destination can be used on macOS for deeper verification.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include SineWaveform/Info.plist.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include SineWaveform/Info.plist.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-sinewaveform-baseline.md` for the canonical
  package and drawing safety baseline.
- See `docs/plans/2026-06-08-versioned-podspec-metadata.md` for the archived
  podspec metadata guard.
- See `docs/plans/2026-06-08-podspec-description-guard.md` for the podspec
  description metadata guard.
- See `docs/plans/2026-06-09-amplitude-clamp.md` for the waveform amplitude
  input guard.
- See `docs/plans/2026-06-09-nan-safe-unit-normalization.md` for the NaN-safe
  level and idle-amplitude normalization guard.
- See `docs/plans/2026-06-09-nonnegative-draw-amplitude.md` for the short-bounds
  draw amplitude guard.
- See `docs/plans/2026-06-09-line-width-clamp.md` for the inspectable stroke
  width guard.
- See `docs/plans/2026-06-09-maximum-wave-count.md` for the draw-time maximum
  wave-count guard.
- See `docs/plans/2026-06-09-phase-accumulator-bound.md` for the bounded phase
  accumulator guard.
- See `docs/plans/2026-06-09-nonnegative-phase-normalization.md` for
  nonnegative phase normalization.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
