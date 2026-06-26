# Semantic Waveform Pixel Fixtures Implementation Plan

Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Add robust UIKit pixel fixtures that distinguish an idle centerline from an active waveform envelope without relying on brittle PNG hashes.

**Architecture:** Extend the existing simulator-only `SineWaveformRenderTests` target and reuse its real `CALayer` rendering path. Convert the rendered image into a one-byte alpha plane, derive the occupied pixel bounds, and assert broad geometry invariants for deterministic single-wave configurations.

**Tech Stack:** Swift 5, UIKit, Core Graphics, XCTest, Python static contracts, Xcode iOS Simulator.

---

### Task 1: Preserve the fixture contract

**Files:**
- Modify: `scripts/check-sinewaveform-source.py`
- Modify: `Tests/ContractCheckerTests/test_waveform_execution_contract.py`

**Step 1: Write the failing source contract**

Require the render test source to contain:

- `testIdleWaveformStaysInCenterPixelBand`
- `testActiveWaveformOccupiesUpperAndLowerPixelBands`
- `alphaBounds(in image: UIImage)`
- assertions that the active fixture reaches both sides of the vertical center

**Step 2: Run the contract test to verify RED**

Run: `scripts/run-python.sh -m unittest Tests.ContractCheckerTests.test_waveform_execution_contract`

Expected: FAIL because the semantic fixtures and alpha-bounds helper are absent.

### Task 2: Add semantic UIKit fixtures

**Files:**
- Modify: `Tests/SineWaveformRenderTests/SineWaveformRenderTests.swift`

**Step 1: Add the idle fixture**

Render an `80 x 40` single-wave view with a transparent background, black
stroke, two-point line width, zero phase shift, and no level update. Assert the
nontransparent pixel bounds remain inside a narrow band around `midY == 20`.

**Step 2: Add the active fixture**

Use the same deterministic view with `frequency = 1`, then call
`updateWithLevel(1)`. Assert occupied pixels reach above `y == 12` and below
`y == 28`, while all four corner pixels remain transparent.

**Step 3: Add the alpha-plane helper**

Draw the rendered `CGImage` into an alpha-only bitmap, scan nonzero bytes, and
return the occupied integral bounds. Return `nil` for a fully transparent image.

**Step 4: Run hosted tests to verify GREEN**

Run: `make check` on the repository's `macos-15` GitHub Actions job.

Expected: the existing five UIKit tests plus the two semantic fixtures pass,
along with the shared waveform math harness and simulator framework build.

### Task 3: Record and land the cycle

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-semantic-waveform-pixel-fixtures.md`

**Step 1: Document the maintained boundary**

Record that hosted rendering covers transparency plus idle and active waveform
geometry, while exact screenshots and physical-device visual QA remain outside
the portable contract.

**Step 2: Run portable validation**

Run package, waveform, contract, root-authority, shell syntax, and diff checks
from the checkout and an external working directory. Record any skipped Swift
or Xcode execution explicitly.

**Step 3: Review and merge**

Push a focused PR, invoke Codex review once, manually review if authentication
is unavailable, require all hosted checks on the exact head, and merge only that
reviewed green commit.

## Verification Evidence

- The waveform checker failed first with five missing semantic-fixture
  guarantees before the UIKit tests were added.
- The completed source checker passed with both fixture names, the alpha-bounds
  helper, and explicit upper/lower active geometry assertions.
- Five contract-checker suites passed after adding four hostile mutations that
  remove the idle fixture, upper assertion, lower assertion, or alpha helper.
- Clean Swift 6/Ruby container `make check` passed from the checkout and an
  external working directory: seven contract suites, 15 executable waveform
  assertions plus their negative control, package/waveform checks, and 147 Make
  authority cases. Xcode rendering and framework build skipped as unavailable.
- Shell syntax and `git diff --check` passed. Hosted exact-head UIKit execution
  remains recorded in `CHANGES.md` as the PR progresses.
