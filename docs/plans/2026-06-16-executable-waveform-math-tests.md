# Executable Waveform Math Tests

Status: Completed

## Goal

Replace static-only confidence in waveform normalization and sample budgeting
with executable tests of the same Swift implementation used by the UIKit view.

## Implementation

- Move finite-value normalization, phase wrapping, sample-step selection, and
  right-edge sample coordinates into `WaveformMath`.
- Keep `SiriWaveformView` responsible for drawing while delegating deterministic
  calculations to the shared helper.
- Compile the helper and a repository-owned Swift test executable with `swiftc`.
- Run the executable through `make test` whenever Swift is available, and make
  the macOS hosted gate execute `make check` so the test cannot be skipped in CI.

## Verification

- `make test` exercises the static contract locally and reports the explicit
  missing-Swift boundary on hosts without `swiftc`.
- Repository and external-directory `make check` passed with the local
  toolchain boundary recorded.
- Hosted macOS `make check` compiles and runs the Swift behavioral harness
  before building the iOS Simulator framework.
- Hostile mutations were rejected for test execution, production delegation,
  NaN fallback, phase wrapping, sample-budget step selection, and exact
  right-edge sampling.
