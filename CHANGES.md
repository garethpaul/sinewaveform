# Changes

## 2026-06-26 14:36 UTC - P2 - Invalidate live waveform rendering properties

### Summary

Closed a UIKit stale-display gap where changing public waveform color or
geometry properties did not request another draw pass.

### Work completed

- Added `setNeedsDisplay()` observers to color, wave count, primary and
  secondary line widths, frequency, and density.
- Preserved the existing level-update semantics for idle amplitude and phase
  shift, which do not alter the current frame until the next update.
- Added a hosted UIKit regression that clears layer invalidation, mutates each
  live rendering property, and requires the layer to become dirty.
- Added portable source contracts, six hostile observer-removal mutations, and
  focused design and implementation records.

### Threads

- Started: live rendering property invalidation — implementation complete.
- Continued: hosted UIKit behavioral verification — pending exact-head CI.
- Stopped: invalidating every inspectable property — rejected because idle
  amplitude and phase shift apply only during the next level update.

### Files changed

- `SineWaveform/SineWaveForm.swift` — invalidates display from six live
  rendering property observers.
- `Tests/SineWaveformRenderTests/SineWaveformRenderTests.swift` — verifies each
  property dirties the backing layer.
- Contract checker, README, VISION, AGENTS, and plans — preserve and document
  the behavior.

### Validation

- RED portable waveform contract — failed on all six missing observers.
- GREEN portable waveform contract — passed after the focused implementation.
- Seven contract-checker suites — passed, including six hostile observer-removal
  mutations.
- Clean Swift 6/Ruby container `make check` from the checkout and `/tmp` —
  passed 147 Make authority cases, package/waveform contracts, 15 executable
  math assertions plus the negative control, and all contract suites.
- Shell syntax and `git diff --check` — passed. Local direct `make check`
  reached the documented missing `/usr/bin/ruby` boundary; Linux skipped Xcode.
- Hosted Check run `28245014338` — passed the contract job in 15 seconds and
  the UIKit tests plus iOS Simulator framework build in 6m47s.
- CodeQL run `28245012697` — passed Actions, Python, and Swift analysis; Swift
  completed in 16m20s.
- Codex review helper — blocked by repeated OpenAI API HTTP 401 failures;
  immutable exact-head manual review found no actionable issues.

### Bugs / findings

- P2: callers could update public properties read directly by `draw(_:)` while
  UIKit continued displaying the previously rendered frame.

### Blockers

- Local Linux lacks Xcode; the hosted macOS simulator remains authoritative for
  the layer invalidation behavior.

### Next action

- Merge PR #17 after the final documentation-only head passes hosted checks.

## 2026-06-26 03:15 PDT - P2 - Add semantic waveform pixel fixtures

### Summary

Expanded the real UIKit rendering suite from compositing-only checks to
deterministic idle and active waveform geometry without brittle PNG hashes.

### Work completed

- Added an idle single-wave fixture that must stay inside the center pixel band.
- Added an active single-wave fixture that must reach upper and lower pixel
  bands while retaining transparent corners.
- Added an alpha-plane bounds helper over the real `CALayer` render output.
- Added source contracts and four hostile fixture-removal mutations.
- Retired the completed broader-pixel-fixture roadmap option; no sample app was
  added.

### Threads

- Started: semantic waveform pixel fixtures — implementation complete.
- Continued: hosted UIKit rendering — awaiting exact-head simulator execution.
- Stopped: exact PNG snapshots — rejected as OS- and antialiasing-brittle.

### Files changed

- `Tests/SineWaveformRenderTests/SineWaveformRenderTests.swift` — adds semantic
  idle/active geometry fixtures and alpha bounds.
- `scripts/check-sinewaveform-source.py` and contract tests — preserve the new
  coverage against deletion.
- README, VISION, AGENTS, and the completed plan — document the boundary.

### Validation

- RED `--mode waveform` — failed on all five missing fixture guarantees.
- GREEN `--mode waveform` — passed.
- Focused contract checker — five suites passed, including four new hostile
  fixture-removal mutations.
- Clean Swift 6/Ruby container `make check` from checkout and `/tmp` — passed
  seven contract suites, 15 executable math assertions plus the negative
  control, package/waveform checks, and 147 Make authority cases.
- Shell syntax and `git diff --check` — passed. Local direct `make check` reached
  the known missing `/usr/bin/ruby` boundary; container Xcode steps skipped.
- Hosted head `ae4f3cb` failed before execution because Swift requires an
  explicit `CGColorSpace` for the bitmap initializer; the helper now uses a
  four-byte device-RGB layout and scans the premultiplied-last alpha byte.
- Hosted UIKit, framework build, CodeQL, review, and merge evidence remains the
  next action for this cycle.

### Bugs / findings

- P2: rendering tests covered transparency and threading but did not verify the
  visible waveform occupied the expected idle and active geometry.

### Blockers

- Local Xcode availability is checked by the canonical Make gate; hosted macOS
  remains authoritative for pixel rendering.

### Next action

- Run portable verification, then require exact-head hosted UIKit tests before
  review and merge.

## 2026-06-26 03:19 UTC - P1 - Own waveform updates on the main thread

### Summary

Made the public level-update API safe for background audio producers without
changing synchronous behavior for callers already on UIKit's main thread.

### Work completed

- Added a main-thread guard that weakly hands background calls to
  `DispatchQueue.main` before phase, amplitude, or redraw mutation.
- Added a UIKit regression test proving the background call returns before
  amplitude changes, main-thread calls remain synchronous, and the queued
  update then applies.
- Added source contracts and hostile mutations for the guard and dispatch.
- Documented the UIKit ownership boundary and focused design decision.

### Validation

- RED: waveform checks rejected the missing guard, dispatch, and reuse path.
- GREEN: clean Ruby 3.3 container gates, seven contract-checker tests, and the
  Swift 5.10 waveform harness with 15 assertions and its negative control pass.
- Hosted Check run `28215127189` passed the synchronous-main/background-handoff
  UIKit regression and framework build in Xcode 16.4; contract validation also passed.
- CodeQL run `28215125327` passed Actions, Python, and Swift analysis.
- The Codex review helper targeted `origin/master` at `21e08c3` and `855b64e`
  but could not authenticate with the OpenAI API (HTTP 401), so both attempts
  were skipped per maintenance policy. After the branch rebased onto the
  provenance correction, the equivalent exact diff passed the expanded gate
  and manual review found no issue.

### Blockers

- No implementation blocker remains; the documentation-only closeout head
  still requires normal hosted checks before merge.

### Next action

- Merge the final hosted-green head and retain both synchronous and handoff tests.

## 2026-06-25 20:10 PDT - P1 - Correct review provenance

### Summary

Corrected the compatibility-matrix review record after pull request #12 merged
with unsupported independent-review claims.

### Work completed

- Replaced unverifiable reviewer counts and independence claims with the Codex
  HTTP 401 result and the exact manual review performed in this maintenance
  session.
- Added a package contract and hostile mutations that reject those unsupported
  provenance phrases in both the change log and completed plan.

### Threads

- None; this is a focused factual correction to merged documentation.

### Files changed

- `CHANGES.md` and the compatibility plan - retain only observed review facts.
- `scripts/check-sinewaveform-source.py` and contract tests - prevent the
  unsupported claims from returning.

### Validation

- The package checker failed first with two unsupported-provenance errors.
- Focused, full, and hosted evidence is recorded before the corrective PR merges.

### Bugs / findings

- P1: Merged review documentation claimed an unsupported reviewer count and
  independence without evidence available in this maintenance session.

### Blockers

- No source or runtime behavior is affected.

### Next action

- Merge the factual correction after package, mutation, hosted, and CodeQL gates
  pass.
## 2026-06-25 19:20 PDT - P2 - Document compatibility boundaries

### Summary

Documented the exact iOS and CocoaPods compatibility matrix without changing
deployment targets, package metadata, tags, public API, or drawing behavior.

### Work completed

- Separated current `master`/Xcode, Git-sourced CocoaPods, public CocoaPods
  trunk, and historical 2016 tag compatibility claims.
- Recorded iOS 12 and Swift 5 as declared floors while treating hosted Xcode
  16.4 simulator execution as evidence rather than an upper support bound.
- Documented that public-trunk installation is unavailable, current CocoaPods
  consumer integration remains unexecuted, and immutable commit pins are the
  reproducible Git source boundary.
- Added package-check contracts for the matrix, maintainer links, and completed
  roadmap item.
- Strengthened the package checker with exact route statuses, all unverified
  boundary bullets, dated Xcode evidence, route-to-status parsing, and fifteen
  hostile matrix mutations covering contradictory content and malformed table
  structure.

### Threads

- Reviewed directly: metadata accuracy — confirmed Xcode, podspec, tag,
  and registry facts.
- Reviewed directly: user guidance — confirmed after CocoaPods wording was
  narrowed to a documented but unverified integration route.
- Reviewed directly: checker quality — iteratively found and closed loose
  status, row, header, separator, and Markdown-table parsing bypasses.

### Files changed

- `docs/compatibility-matrix.md` - route-by-route compatibility and validation
  matrix.
- `scripts/check-sinewaveform-source.py` - static matrix and documentation
  synchronization contracts.
- `Tests/ContractCheckerTests/test_waveform_execution_contract.py` - hostile
  compatibility-matrix mutations.
- README, vision, agent guidance, and design/implementation plans - preserve the
  declared-versus-verified boundary.

### Validation

- The direct package checker failed first with one missing matrix contract.
- Direct package and waveform checks plus six contract-checker tests passed.
- All four Make aliases and external-directory `make check` passed in a clean
  Debian container with Ruby; Swift and Xcode execution skipped as unavailable.
- The official CocoaPods package list returned HTTP 200 with no `SineWaveform`
  entry, the package page returned HTTP 404, and tag podspec facts matched the
  documented historical boundaries.
- Hosted Check run `28213048100` passed the portable contract lane, four UIKit
  simulator tests, shared Swift math harness, and framework build with Xcode
  16.4 on commit `a420ee67f84d74f1d036267c7c2e23688c5fc5ae`.
- CodeQL run `28213046910` passed Actions, Python, and Swift analysis.
- The Codex review helper targeted `origin/master` at `a420ee6` but could not
  authenticate with the OpenAI API (HTTP 401). The final exact diff was reviewed
  manually with no actionable findings.

### Bugs / findings

- P2: Existing installation notes did not provide one exact matrix separating
  current source, historical tags, public registry state, and executed tests.
- P2: The first checker accepted contradictory availability claims and did not
  bind Xcode 16.4 to a dated hosted observation; both gaps are closed.

### Blockers

- No implementation blocker remains; the corrected head still requires normal
  hosted checks before merge. CocoaPods consumer integration, physical devices,
  publication, and future toolchain ceilings remain explicitly unverified.

### Next action

- Add a sample application or broader pixel snapshot fixtures without changing
  the compatibility floor implicitly.

## 2026-06-25 17:13 PDT - P2 - Harden transparent rendering verification

### Summary

Closed the final review gaps in pull request #11 by making initializer checks
mutation-sensitive, selecting iOS Simulator runtimes numerically, and rendering
the real view layer in the UIKit alpha tests.

### Work completed

- Strengthened the decoded-view test by archiving an explicitly opaque source
  view before verifying `init(coder:)` restores nonopaque compositing.
- Replaced direct `draw(_:)` test invocation with normal `CALayer` rendering
  and added a translucent-background alpha assertion.
- Replaced lexicographic simulator runtime ordering with numeric version tuples
  and rejected runtimes below the iOS 12 deployment target.
- Replaced the two-occurrence opacity contract with initializer-specific
  structural checks and hostile comment-only mutations.

### Threads

- Reviewed: Xcode target integrity — confirmed the XCTest source, framework
  dependency, shared scheme, Make entry point, and hosted workflow are wired.
- Reviewed: adversarial implementation pass — accepted the coder-contract and
  simulator-order findings. Hosted rendering proved the layer-only background
  attempt was cleared by `draw(_:)`, so the passing conditional fill returned.

### Files changed

- `Tests/SineWaveformRenderTests/SineWaveformRenderTests.swift` — uses real
  layer rendering and covers decoded override plus translucent backgrounds.
- `Tests/ContractCheckerTests/test_waveform_execution_contract.py` — rejects
  opacity assignments moved into comments.
- `Tests/ContractCheckerTests/test_select_ios_simulator.py` — covers numeric
  runtime ordering and the deployment-target floor.
- `scripts/check-sinewaveform-source.py` — validates each initializer and the
  stronger render-test boundary.
- `scripts/select-ios-simulator.py` — parses and sorts numeric iOS versions.
- `CHANGES.md` and the completed rendering plan — record review evidence.

### Validation

- Initial Python contract run — failed on both simulator fixtures and both
  comment-only opacity mutations; the old static contract also rejected the
  proposed UIKit-owned background implementation.
- Corrected Python contract run — five tests passed; package and waveform source
  checks passed.
- Temporary hosted run `28208410926` — four UIKit tests and the framework build
  passed on `macos-15` with the conditional background fill.
- Exact-head run `28208773112` — the layer-only attempt failed the translucent
  assertion with alpha `0`, proving the post-clear fill remains required.
- Local `make check` — passed 147 target/authority cases, one dollar-syntax
  checkout case, two `MAKEFILE_LIST` rejections, three startup-boundary cases,
  and ten mode-flag rejections before stopping at missing `/usr/bin/ruby`.
- Codex review helper at `d86f78c` raised an integer-accuracy compile concern;
  hosted Xcode 16.4 compiled and executed that assertion, so the finding was
  rejected. The same run exposed the separate alpha regression above.
- Implementation head `4b6f667` — exact-head Codex review reported no
  actionable findings; hosted run `28209032847` passed the contract lane and
  all four UIKit rendering tests plus the iOS Simulator framework build.

### Bugs / findings

- P2 fixed: comment-only `isOpaque = false` text could satisfy the previous
  occurrence-count contract without protecting either initializer.
- P3 fixed: lexicographic runtime ordering selected iOS 18.9 before iOS 18.10
  and allowed unsupported pre-iOS-12 runtimes.
- P2 fixed: removing the conditional background fill caused `draw(_:)` to clear
  the layer-owned color and render alpha `0`; the restored fill preserves 50%
  alpha while the nil-background test remains transparent.

### Blockers

- None in the implementation; the final documentation-only head must retain
  the same green review and hosted-check state before merge.

### Next action

- Revalidate the documentation-only head, merge PR #11, and synchronize
  `master`.

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
- Restored an explicitly assigned background after the context clear while
  leaving a nil background transparent.
- Added static and mutation-sensitive contracts for the test target, runner,
  and compositing implementation.

### Threads

- Started: none; the focused UIKit defect was completed directly.
- Reviewed: external review-gap commit `debc388` — accepted its simulator
  selector, comment-bypass, and decoded-state findings; added the translucent
  background assertion as stronger coverage without claiming a reproduced bug.
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
- Review-gap tests at `debc388` failed on lexical iOS runtime ordering,
  unsupported pre-iOS-12 selection, and comment-only opacity assignments.
- Temporary run `28208410926` passed the translucent test with the conditional
  fill; exact-head run `28208773112` failed with alpha `0` after its removal,
  so the conditional post-clear fill was restored.
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
