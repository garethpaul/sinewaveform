# Installation Naming

## Status: Completed

## Priority

1. State the exact CocoaPods package and Swift module name.
2. Show the public waveform view type and update method without ambiguity.
3. Use a version/tag that matches the publishable root podspec.
4. Reject lowercase package/import examples that do not match the module.

## Context

The README described cloning and opening the Xcode project but did not provide
a Podfile entry, Swift import, or minimal construction example. The repository
name is lowercase, the package/module is `SineWaveform`, the source file has
historical `SineWaveForm.swift` capitalization, and the public class is
`SiriWaveformView`; readers could reasonably choose the wrong identifier.

## Requirements

- R1. Add a CocoaPods Git/tag example aligned with root podspec version 0.0.6.
- R2. Show `import SineWaveform` and reject lowercase imports.
- R3. Show `SiriWaveformView` construction and `updateWithLevel(_:)` usage.
- R4. Explain the repository, module, source-file, and public-type names.
- R5. Add static contracts and synchronize roadmap and maintenance guidance.

## Verification Plan

- Prove the package checker fails before README installation content exists.
- Run package and source checks directly.
- Run `make check` from the repository and an external directory.
- Review exact hosted Swift/Xcode and CodeQL evidence.

## Scope Boundaries

- Do not publish a pod, change podspec metadata, or claim CocoaPods trunk state.
- Do not rename files, modules, targets, or public Swift types.
- Do not change waveform drawing or public API behavior.
- Do not claim local Xcode execution from Linux.

## Work Completed

- Added exact package, module, type, and usage guidance.
- Added static positive and incorrect-lowercase naming contracts.
- Synchronized roadmap and maintenance guidance.

## Verification

- The package checker failed before README installation content was added on
  2026-06-25.
- Lowercase import, wrong tag, and wrong public-type mutations were rejected on
  2026-06-25.
- Full `/usr/bin/make check` passed 133 Make authority cases, then stopped
  because the pinned `/usr/bin/ruby` is unavailable on this Linux host.
- Root and external-directory `make root-test contract-test test` passed 133
  authority cases, three execution-contract tests, and waveform checks;
  standalone Swift execution skipped because no approved compiler exists.
- Direct package/waveform checks, Python compilation, and `git diff --check`
  passed. Hosted macOS remains authoritative for Ruby, Swift, and Xcode.
