# Transparent Waveform Rendering Design

## Status: Completed

## Evidence

- `SiriWaveformView.draw(_:)` clears its bounds, conditionally selects
  `backgroundColor`, and then always fills the dirty rectangle. When the
  background is `nil`, that unconditional fill uses the graphics context's
  current fill state instead of preserving transparency.
- The view does not set `isOpaque = false`, although its default configuration
  has no background color and draws partially transparent content.
- The project has executable pure-math coverage but no UIKit rendering test or
  sample target, matching the open visual-verification risk in `.explore` and
  `VISION.md`.
- Apple documents that `UIGraphicsImageRendererFormat.opaque = false` supplies
  an alpha channel and that custom views containing transparent content must
  set `isOpaque` to false:
  - https://developer.apple.com/documentation/uikit/uigraphicsimagerendererformat/opaque
  - https://developer.apple.com/documentation/uikit/uiview/1622622-opaque
- Apple documents `xcodebuild test` as the command-line execution boundary for
  XCTest suites:
  https://developer.apple.com/documentation/xcode/running-tests-and-interpreting-results

## Approaches Considered

1. **Pure helper contract** — extract a Boolean that decides whether to fill.
   This is portable, but it does not exercise UIKit, the graphics context, or
   the view's opacity flag, so it would leave the actual rendering bug indirect.
2. **Sample application** — add an app target for manual visual inspection.
   This improves discoverability but does not create repeatable failure evidence
   and is larger than the defect requires.
3. **Simulator XCTest render probe** — add a logic-test target that renders the
   real view into an alpha-enabled image and samples a pixel. This directly
   covers UIKit behavior and gives hosted CI an automated visual boundary.

## Decision

Use the simulator XCTest render probe. The test target imports the framework,
asserts that a newly created waveform view is nonopaque, and renders a view with
a nil background and clear wave color into a one-scale alpha-enabled image. A
center pixel must remain transparent.

The production change is deliberately small: initialize both programmatic and
Interface Builder instances with `isOpaque = false`, clear the drawing context,
and fill only when an explicit background color is assigned.

## Validation

- Hosted simulator tests must fail on the unmodified implementation for the
  opacity and alpha assertions.
- The same tests must pass after the minimal implementation.
- Existing math, package, Make-authority, simulator-build, and CodeQL gates must
  remain green.
- Static contracts must require the test target, test runner, and nonopaque
  initialization so future project-file or recipe drift cannot silently remove
  the rendering boundary.

Hosted `make check` failed with all three expected assertions before the
production change, then passed after the minimal compositing fix.
