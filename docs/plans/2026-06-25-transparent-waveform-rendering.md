# Transparent Waveform Rendering Implementation Plan

## Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Preserve transparency for the default waveform view and verify the real UIKit drawing path on an iOS Simulator.

**Architecture:** Add a framework logic-test target and shared scheme to the existing Xcode project. A repository runner selects an available iPhone Simulator and executes XCTest from `make test`; the production view then adopts nonopaque compositing and removes the unconditional background fill.

**Tech Stack:** Swift 5, UIKit, XCTest, Core Graphics, Xcode 16 on `macos-15`, GNU Make, Python static contracts.

---

### Task 1: Add the UIKit rendering test boundary

**Files:**
- Create: `Tests/SineWaveformRenderTests/SineWaveformRenderTests.swift`
- Create: `scripts/run-ios-render-tests.sh`
- Create: `SineWaveform.xcodeproj/xcshareddata/xcschemes/SineWaveform.xcscheme`
- Modify: `SineWaveform.xcodeproj/project.pbxproj`
- Modify: `Makefile`
- Modify: `scripts/check-sinewaveform-source.py`
- Modify: `Tests/ContractCheckerTests/test_waveform_execution_contract.py`

**Step 1: Write the failing tests**

Add one XCTest asserting `SiriWaveformView(frame:).isOpaque == false` and one
that calls `draw(_:)` inside an alpha-enabled `UIGraphicsImageRenderer`, samples
the center pixel through a known RGBA bitmap context, and expects zero alpha.

**Step 2: Make hosted execution authoritative**

Add the test bundle target, framework dependency, shared test scheme, simulator
selection runner, and conditional `make test` invocation. Extend static and
mutation contracts to require a real runner execution.

**Step 3: Verify RED**

Run portable checks locally, push the test-only branch, and run the hosted
`macos-15` matrix. Expected: the new simulator XCTest suite fails because the
view is opaque and the nil-background render has a nonzero alpha pixel.

### Task 2: Implement transparent compositing

**Files:**
- Modify: `SineWaveform/SineWaveForm.swift`

**Step 1: Implement the minimal fix**

Add programmatic and coder initializers that set `isOpaque = false`. Remove the
manual background-color selection and unconditional `context.fill(rect)` from
`draw(_:)`; keep the existing bounds validation and context clear.

**Step 2: Verify GREEN**

Run focused static/portable checks, push, and require the hosted simulator test,
framework build, and CodeQL lanes to pass.

### Task 3: Record and land the cycle

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `AGENTS.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-25-transparent-waveform-rendering.md`

**Step 1: Document behavior and evidence**

Record default transparency, the simulator rendering command, the red failure,
all local and hosted checks, hostile mutations, review findings, and remaining
device/snapshot risk.

**Step 2: Review and merge**

Open a focused PR, run exact-head Codex review, fix all actionable findings,
wait for green hosted checks, merge to `master`, and persist `.explore` plus the
global repository indexes.

## Verification Evidence

- RED head `f515bd2`: hosted `make check` executed three UIKit tests; default
  and decoded views were opaque, and the nil-background pixel alpha was `255`.
- GREEN head `0a48af8`: the same hosted simulator suite and framework build
  passed after the two initializer flags and conditional background fill.
- Portable package, waveform, contract, and 147-case root-authority checks passed; local
  full `make check` stops at the known missing `/usr/bin/ruby` boundary.
