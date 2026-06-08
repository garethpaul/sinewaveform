## SineWaveform Vision

SineWaveform is a Swift UIView subclass that draws an animated sine-wave style
waveform, configurable through Interface Builder and code.

The repository is useful as a small reusable UI component with inspectable
properties for color, wave count, line widths, amplitude, frequency, density,
and phase shift.

The goal is to keep the waveform component lightweight, packageable, and easy
to preview in both storyboard/XIB and programmatic use.

The current focus is:

Priority:

- Preserve the `SiriWaveformView` drawing behavior
- Keep Interface Builder inspectables useful
- Maintain screenshot and GIF examples
- Treat CocoaPods and Swift syntax as legacy until documented

Next priorities:

- Fix README installation naming and import examples
- Document supported Swift, iOS, and CocoaPods versions
- Add a simple sample app or snapshot verification path
- Modernize drawing APIs in a dedicated compatibility pass

Contribution rules:

- One PR = one focused drawing, API, packaging, sample, or documentation change.
- Keep public inspectable properties stable unless documented.
- Include visual verification for drawing changes.
- Do not add network or analytics behavior to the component.

## Security And Responsible Use

This should remain a local UI component. It should not collect audio,
microphone data, or usage analytics; callers should decide how input levels are
computed and supplied.

## What We Will Not Merge (For Now)

- Microphone capture inside the view
- Hidden telemetry
- Public API changes without migration notes
- Visual rewrites without screenshot or sample verification

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
