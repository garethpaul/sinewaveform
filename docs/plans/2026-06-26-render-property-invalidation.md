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
- Hosted UIKit/Xcode, CodeQL, and exact-head review evidence remain to be
  recorded before merge.
