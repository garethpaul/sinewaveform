# sinewaveform

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Device Preview

<!-- DEVICE-PREVIEW-IMAGE -->
![Device preview](docs/device-preview.svg)

## Overview

`garethpaul/sinewaveform` is a reusable Swift view that renders a Siri-style animated waveform for Apple platforms.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C/C++ headers (1), Swift (3).

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
  waveform drawing safety checks for context availability, finite positive
  bounds, wave count, and draw step handling. When `xcodebuild` is installed,
  the `build` target also builds the `SineWaveform` target for the iOS simulator.
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
- Static waveform checks also require frequency, density, line widths, and
  phase shift to pass through shared finite-range normalization before drawing;
  negative frequency remains supported for mirrored waveforms.
- Static waveform checks also require the final horizontal sample to be
  clamped to the right view edge so draw geometry never extends past bounds.
- An exact 4,096-point waveform sample budget includes both path endpoints
  while retaining the configured density for normal view widths.
- Static waveform checks reject non-finite view dimensions before Core Graphics
  mutations, division, or horizontal sampling.
- Subnormal waveform widths are rejected before Core Graphics mutation, and
  envelope scaling avoids a separately overflowing reciprocal.
- Static package checks cover the root and archived versioned podspec metadata.
- Static package checks require the publishable root podspec to declare Swift 5
  and the same iOS 12 minimum as the hosted Xcode build; archived release
  podspec snapshots retain their historical compatibility metadata.
- Static package checks reject empty placeholder podspec descriptions before
  the real package description.
- Static package checks also require completed canonical plans under `docs/plans`.
- GitHub Actions runs portable package and waveform checks on Ubuntu 24.04. On
  macOS 15 it also compiles and runs the shared Swift waveform math tests before
  building the framework for a generic iOS Simulator.
- Xcode builds use the shared `SineWaveform` scheme and place DerivedData under
  `/tmp/sinewaveform-derived-data` so caller variables cannot redirect build
  artifacts into the repository or another sensitive path.
- The single approved workflow uses immutable actions, read-only permissions,
  and checkout with persisted GitHub credentials disabled in both jobs.
- The Xcode project uses Swift 5 language mode and targets iOS 12 or newer.
- `make test` runs the executable Swift behavioral harness when `swiftc` is
  available and reports an explicit skip on hosts without that toolchain.

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
- See `docs/plans/2026-06-10-finite-inspectable-inputs-and-ci.md` for bounded
  inspectable floating-point inputs and the CI gate.
- See `docs/plans/2026-06-10-right-edge-sample-clamp.md` for bounded
  right-edge waveform sampling.
- See `docs/plans/2026-06-13-waveform-sample-budget.md` for the waveform sample
  budget on pathological finite view widths.
- See `docs/plans/2026-06-14-make-root-override-protection.md` for authoritative
  repository-root selection across all Make aliases.
- See `docs/plans/2026-06-21-make-authority-isolation.md` for checked-in recipe
  authority, hostile-input coverage, and the GNU Make startup boundary.
- See `docs/plans/2026-06-14-exact-waveform-sample-budget.md` for the exact
  endpoint-inclusive per-wave point budget.
- See `docs/plans/2026-06-16-executable-waveform-math-tests.md` for the shared
  production math and executable Swift behavioral gate.
- See `docs/plans/2026-06-17-subnormal-width-geometry.md` for the midpoint
  underflow guard and overflow-safe envelope scaling.
- See `docs/plans/2026-06-19-temp-xcode-artifacts.md` for the temp Xcode
  artifact contract.
- See `docs/plans/2026-06-19-waveform-test-execution-contract.md` for the
  static guarantee that the compiled waveform math test binary is executed.
- See `docs/plans/2026-06-12-root-podspec-toolchain-alignment.md` for the
  publishable CocoaPods/Xcode compatibility contract.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
