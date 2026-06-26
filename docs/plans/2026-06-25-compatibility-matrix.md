# Compatibility Matrix Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Document the exact iOS, Swift, Xcode, CocoaPods, and historical-tag compatibility boundaries for SineWaveform.

**Architecture:** Add one route-based compatibility matrix sourced from podspec, Xcode, tag, official CocoaPods index, and hosted-check evidence. Link it from maintainer-facing documents and enforce its distinctions with the existing Python package checker.

**Tech Stack:** Markdown, Python static contracts, CocoaPods podspec metadata, Xcode project settings, Git tag evidence.

---

## Status: Completed

### Task 1: Establish the failing matrix contract

**Files:**
- Modify: `scripts/check-sinewaveform-source.py`
- Add: `docs/plans/2026-06-25-compatibility-matrix-design.md`
- Add: `docs/plans/2026-06-25-compatibility-matrix.md`

1. Require the design, plan, and compatibility matrix files.
2. Require separate current-source, Git CocoaPods, public trunk, historical-tag,
   declared-requirement, and executed-evidence boundaries.
3. Run `make check`; expect failure because the matrix and synchronized links do
   not exist.

### Task 2: Publish exact compatibility guidance

**Files:**
- Add: `docs/compatibility-matrix.md`

1. Record iOS 12 and Swift 5 as current declared floors.
2. Record Xcode 16.4 simulator execution as evidence, not a maximum supported
   Xcode or SDK version.
3. Explain that Git-sourced CocoaPods uses the current root podspec but public
   trunk installation is unavailable and all 2016 tags are historical.
4. List unverified paths and the commands/evidence needed to promote them.

### Task 3: Synchronize repository guidance

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `AGENTS.md`
- Modify: `CHANGES.md`

1. Link the matrix from installation and maintainer guidance.
2. Remove the completed roadmap priority without changing later priorities.
3. Record the documentation-only change and its release boundaries.

### Task 4: Verify and ship

**Files:**
- Modify: `docs/plans/2026-06-25-compatibility-matrix.md`

1. Run package checks, full Make aliases, diff, artifact, and credential audits.
2. Open a focused PR and run exact-base Codex review.
3. Require hosted macOS, contract, and CodeQL checks before merge.

## Verification Completed

- The direct package checker failed first with one validation error because
  `docs/compatibility-matrix.md` was absent.
- The matrix now separates declarations, executed evidence, historical tags,
  public registry state, and unverified integration paths.
- README, vision, agent, and change-log guidance link the matrix, and the
  completed first roadmap priority was removed.
- `make check` remains blocked locally at the repository's pinned
  `/usr/bin/ruby` boundary; narrow package, contract, waveform, and hosted gates
  provide the remaining verification before merge.
- Direct package and waveform checks passed, along with all six Python
  contract-checker tests.
- In a clean Debian container with `/usr/bin/ruby`, `make check`, `make lint`,
  `make test`, `make build`, and external-directory `make check` passed. Swift
  and Xcode execution skipped because those Apple toolchains were unavailable.
- The official CocoaPods package list returned HTTP 200 without a
  `SineWaveform` entry, the package page returned HTTP 404, and repository tag
  podspecs confirmed the documented 0.0.6/iOS 8 and 0.1.0/0.0.1 mismatches.
- Fifteen hostile matrix mutations proved the checker rejects contradictory public
  trunk and Git-integration statuses, removed unverified boundaries, missing
  dated Xcode evidence, missing floating-runner caveats, and statuses attached
  to the wrong route or hidden behind duplicate, unexpected, malformed, or
  no-space or outer-pipe-free Markdown rows, a malformed header, and a missing
  table separator, and contradictory status or evidence suffixes.
- Final hosted macOS and CodeQL results remain the merge boundary for the
  corrected head.
- Hosted Check run `28213048100` passed the portable contract lane, shared Swift
  math harness, four UIKit simulator tests, and framework build with Xcode 16.4
  (16F6) on commit `a420ee67f84d74f1d036267c7c2e23688c5fc5ae`.
- CodeQL run `28213046910` passed Actions, Python, and Swift analysis.
- The Codex review helper selected the PR base `origin/master` but failed with
  HTTP 401 authentication errors. Per the maintenance instruction, that review
  was skipped; exact-head manual review found no actionable findings.
