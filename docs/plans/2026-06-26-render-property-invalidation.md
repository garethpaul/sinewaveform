# Render Property Invalidation Implementation Plan

Status: Completed

1. Add the failing UIKit and source contracts.
2. Add focused `didSet` display invalidation.
3. Add mutation-sensitive documentation contracts.
4. Run portable and hosted verification.
5. Review and merge the exact head.

## Verification Evidence

- The portable waveform contract failed first on all six missing observers.
- The source contract passes with focused `didSet` invalidation on exactly the
  properties read directly by `draw(_:)`.
- Seven contract-checker suites pass, including six hostile observer-removal
  mutations.
- Clean Swift 6/Ruby container `make check` passed from the checkout and an
  external working directory: 147 Make authority cases, package and waveform
  contracts, 15 executable math assertions plus the negative control, and all
  contract suites. Xcode execution skipped as unavailable in Linux.
- Local shell syntax and `git diff --check` passed; direct local `make check`
  reached the documented missing `/usr/bin/ruby` boundary.
- Hosted Check run `28245014338` passed the contract job in 15 seconds and the
  UIKit tests plus iOS Simulator framework build in 6m47s.
- CodeQL run `28245012697` passed Actions, Python, and Swift analysis; Swift
  completed in 16m20s.
- The Codex review helper was attempted and blocked by repeated OpenAI API HTTP
  401 failures; immutable exact-head manual review found no actionable issues.
