# Compatibility Matrix Design

## Status: Completed

## Problem

The README explains how to consume the default branch through CocoaPods, but
readers still have to infer which iOS floor, Swift language mode, Xcode evidence,
tag history, and public CocoaPods availability apply to each installation path.
Those are different claims: current project settings do not rewrite historical
tags, and a syntactically valid root podspec does not prove public trunk
publication or a complete `pod install` integration.

## Evidence

- The root podspec declares version 0.0.6, iOS 12.0, and Swift 5.0.
- Every Xcode target configuration retains iOS 12.0 and Swift 5.0 settings.
- Hosted `macos-15` verification has compiled the framework and run UIKit
  simulator tests with Xcode 16.4.
- Repository tags 0.0.2 through 0.1.0 all point to July 9, 2016 commits. The
  0.0.6 tag advertises iOS 8.0 with no Swift-version declaration, and the 0.1.0
  tag contains a podspec whose internal version is 0.0.1.
- The official CocoaPods CDN index did not contain `SineWaveform`, and
  <https://cocoapods.org/pods/SineWaveform> returned 404 on June 25, 2026.

## Options

1. State one broad supported range. This would conflate current source,
   historical tags, CocoaPods metadata, and hosted build evidence.
2. Update or publish a tag as part of the documentation work. This would turn a
   compatibility clarification into an unverified release.
3. Publish a route-by-route matrix that distinguishes declared requirements,
   executed evidence, historical metadata, and unverified boundaries.

## Decision

Use option 3. Document direct Xcode/default-branch use, Git-sourced CocoaPods,
public CocoaPods trunk, and historical tags separately. Treat iOS 12 and Swift
5 as the current declared floor, Xcode 16.4 as evidence rather than a maximum,
and all 2016 tags as historical snapshots rather than current releases.

## Boundaries

- Do not publish or retag a CocoaPod in this change.
- Do not claim public CocoaPods installation while the official index has no
  package entry.
- Do not claim `pod install`, `pod lib lint`, physical-device, or App Store
  compatibility without executing those paths.
- Do not change the iOS deployment target, Swift language mode, podspec version,
  public API, or drawing behavior.
- Recommend an exact reviewed commit instead of a mutable branch for
  reproducible Git-sourced CocoaPods use.

## Verification

Add a package-check contract for the matrix, repository-document links, roadmap
completion, and explicit declared-versus-verified language. Run `make check`
before and after the guide, then preserve hosted Xcode evidence without turning
one Xcode version into a support ceiling.
