# Changes

## 2026-06-25 16:54 PDT - P1 - Preserve default waveform transparency

### Summary

Added an executable UIKit rendering boundary and fixed the waveform view's
default compositing. Programmatic and decoded instances are now nonopaque, and
a nil background no longer becomes an implicit opaque context fill.

### Work completed

- Added an iOS Simulator XCTest target and shared scheme that render the real
  `SiriWaveformView` and inspect pixel alpha.
- Added repository-owned simulator selection and test execution to `make test`.
- Set `isOpaque = false` in frame and coder initialization paths.
- Left assigned background-color compositing to the UIKit layer so translucent
  colors are applied exactly once.
- Added static and mutation-sensitive contracts for the test target, runner,
  and compositing implementation.

### Threads

- Started: none; the focused UIKit defect was completed directly.
- Reviewed: external review-gap commit `debc388` — accepted its simulator
  selector, comment-bypass, decoded-state, and translucent-background findings.
- Continued: none.
- Stopped: none.

### Files changed

- `SineWaveform/SineWaveForm.swift` — preserves transparent compositing.
- `Tests/SineWaveformRenderTests/SineWaveformRenderTests.swift` — verifies
  programmatic, decoded, and pixel-alpha behavior.
- `SineWaveform.xcodeproj` — adds the test bundle and shared test scheme.
- `scripts/run-ios-render-tests.sh` and `scripts/select-ios-simulator.py` — run
  the hosted simulator boundary deterministically.
- `Makefile`, static checks, guidance, and plans — wire and document the gate.

### Validation

- RED hosted `make check` at `f515bd2` — all three UIKit tests failed for the
  intended behavior: both views were opaque and transparent pixel alpha was
  `255` rather than `0`.
- GREEN hosted `make check` at `0a48af8` — simulator rendering tests and the
  iOS framework build passed.
- Review-gap tests at `debc388` then failed on lexical iOS runtime ordering,
  unsupported pre-iOS-12 selection, comment-only opacity assignments, and a
  double-composited translucent background; all findings were accepted.
- Local package, waveform, contract, and 147-case root-authority checks passed;
  Swift and Xcode execution skipped because approved host tools are absent.
- Local full `make check` reached the known `/usr/bin/ruby` absence after the
  root-authority gate; hosted macOS remains authoritative for Ruby and UIKit.

### Bugs / findings

- P1: a default nil-background waveform cleared its context and then filled it
  with the implicit current fill color, producing opaque output.
- P2: the view retained UIKit's opaque default across both initialization paths.
- P2: lexical runtime sorting preferred iOS 18.9 over 18.10 and did not filter
  simulators below the framework's iOS 12 deployment target.

### Blockers

- None for the implementation; exact-head review and final hosted checks remain
  required before merge.

### Next action

- Run hostile mutations and exact-head Codex review, then merge only with all
  hosted checks green.

## 2026-06-25 11:54 PDT - P2 - Clarify package, module, and public type names

### Summary

Added an exact repository-backed CocoaPods installation example and minimal
Swift usage snippet. The README now distinguishes the lowercase repository,
`SineWaveform` pod/module, historical `SineWaveForm.swift` filename, and public
`SiriWaveformView` type.

### Work completed

- Added a default-branch Git Podfile entry that consumes the current root
  podspec instead of the stale historical 0.0.6 tag.
- Added `import SineWaveform`, view construction, and level-update examples.
- Added positive and incorrect-lowercase naming contracts plus completed plan
  evidence and roadmap synchronization.

### Threads

- Started: none; the focused documentation gap was completed directly.
- Continued: none.
- Stopped: none.

### Files changed

- `README.md` — added installation, naming, import, and usage guidance.
- `scripts/check-sinewaveform-source.py` — enforced exact documented names.
- `VISION.md` — removed the completed installation priority.
- `AGENTS.md` — recorded the naming boundary for future maintenance.
- `docs/plans/2026-06-25-installation-naming.md` — recorded scope and evidence.

### Validation

- Initial red package check — failed fast on the missing completed plan.
- Second red package check — after adding scope evidence, reported all seven
  missing README installation/import fragments.
- First focused rerun — package validation found the required public-type phrase
  split across a Markdown line break; corrected the wording. The attempted
  `--mode source` command also failed because the valid mode is `waveform`.
- Initial exact-head Codex review — found the proposed 0.0.6 tag resolves to an
  older iOS 8/HTTP podspec rather than the current checked-in metadata.
- Corrected the example to `:branch => 'master'`, documented its non-immutable
  boundary, and explicitly rejected the stale 0.0.6 tag form.
- Three hostile README mutations — lowercase import, stale tag, and wrong
  public type were each rejected for the intended contract violation.
- Full `/usr/bin/make check` — passed 133 Make authority cases, then stopped at
  podspec syntax because this host lacks the pinned `/usr/bin/ruby`.
- Root and external-directory `make root-test contract-test test` — passed 133
  authority cases, three execution-contract tests, and waveform checks; Swift
  execution skipped truthfully because no approved `swiftc` exists locally.
- Direct package/waveform checks, Python compilation, and `git diff --check` —
  passed. Hosted Ruby, Swift, and Xcode validation remains pending.
- CocoaPods installation — not executed; the example targets the current
  default branch, explains commit pinning for reproducibility, and does not
  claim public trunk availability.

### Bugs / findings

- P2: users could confuse the lowercase repository name, pod/module name,
  historical source filename, and public view type because no install or import
  example existed.

### Blockers

- CocoaPods and Xcode are unavailable on this Linux host; hosted build evidence
  remains authoritative for the framework target.

### Next action

- Open the pull request, run exact-head review, and require hosted podspec,
  Swift execution, Xcode build, and CodeQL success before merge.

## 2026-06-21

- Isolated repository verification from caller-controlled Make variables,
  hostile `PATH` entries, and whitespace-sensitive checkout roots.
- Rejected non-executing Make modes and trailing additional Makefiles before
  they can bypass or replace repository verification recipes.

## 2026-06-19

- Xcode builds now use the shared scheme and put DerivedData under a temporary
  location, keeping local and CI build artifacts out of user-global locations.
- Static package verification now rejects waveform test runners that compile
  the behavioral harness without executing the resulting binary.

## 2026-06-17

- Subnormal waveform widths are rejected before Core Graphics mutation, with
  overflow-safe envelope scaling for tiny nonzero midpoints.

## 2026-06-16

- Added executable Swift tests for waveform normalization, phase wrapping, and
  exact sample-budget coordinates, using the same helper as the UIKit view.

## 2026-06-14

- Made the exact 4,096-point waveform sample budget include both left and right
  endpoint samples by budgeting 4,095 intervals.

## 2026-06-13

- Added a waveform sample budget of approximately 4,096 horizontal points per
  path while preserving configured density and the exact right-edge sample.

## 2026-06-12

- Rejected non-finite view dimensions before waveform geometry and sampling so
  invalid bounds cannot produce non-terminating draw work.
- Aligned the publishable root podspec with the hosted Swift 5 and iOS 12
  framework build while preserving archived release metadata.

## 2026-06-10

- Added a fixed macOS 15 CI job that builds the framework for a generic iOS
  Simulator and fixed portable checks to Ubuntu 24.04.
- Disabled persisted checkout credentials and made the two-job workflow an
  exact single-file repository contract.
- Updated the project to Swift 5 and iOS 12 and migrated the waveform view to
  current UIKit and Core Graphics APIs.
- Made Makefile verification and build paths independent of the caller's
  working directory.
- Bounded inspectable frequency, density, line widths, and phase shift through
  shared NaN-safe normalization before drawing.
- Preserved the declared idle-amplitude and phase-shift defaults when
  Interface Builder supplies NaN values.
- Added a least-privilege Python 3.12 GitHub Actions gate for portable checks.
- Clamped the final waveform sample to the right view edge so coarse density
  steps cannot produce off-bounds geometry or a negative edge envelope.

## 2026-06-09

- Centralized unit-interval normalization for level and idle-amplitude inputs
  so `NaN` values fall back before updating draw amplitude.
- Shifted negative `fmod` phase remainders into the nonnegative sine cycle and
  added static validation for normalized phase range correction.
- Wrapped waveform phase accumulation to a single sine cycle so long-running
  updates do not grow `_phase` without bound.
- Capped draw-time wave counts so excessive `numOfWaves` inspectable values do
  not create unbounded rendering work.
- Clamped inspectable waveform line widths at draw time before passing them to
  Core Graphics.
- Clamped draw-time maximum amplitude to a nonnegative value so very short
  bounds do not invert waveform rendering.
- Clamped `updateWithLevel` input levels and `idleAmplitude` into the expected
  `0...1` waveform drawing range.
- Extended waveform static checks to preserve bounded amplitude assignment.

## 2026-06-08

- Removed empty placeholder podspec descriptions and added static package
  validation for non-empty description metadata.
- Aligned archived versioned podspec URLs with the root HTTPS/lowercase package
  metadata and extended static package checks across all tracked podspecs.
- Added `make check` as the shared repository verification alias.
- Guarded `drawRect` against missing graphics contexts and zero-size bounds.
- Changed the wave loop to draw within the clamped wave count instead of one
  extra wave.
- Extended the waveform checker to protect context, bounds, and loop-count
  contracts.
- Added a Makefile verification gate for podspec syntax, package metadata, and
  waveform drawing safety.
- Updated root CocoaPods metadata URLs to HTTPS and matched the GitHub repo URL
  casing.
- Guarded waveform drawing against zero wave counts and non-positive density
  steps from Interface Builder/runtime configuration.
- Documented local verification steps.
- Added canonical `docs/plans` coverage and made package checks require
  completed plans.
