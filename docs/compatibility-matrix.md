# SineWaveform Compatibility

## Compatibility Matrix

This matrix separates requirements declared by checked-in metadata from paths
that have actually executed. It applies to the repository state on June 25,
2026; it does not retroactively change the 2016 tags or create a CocoaPods
release.

| Consumption route | Declared requirement or metadata | Executed evidence | Status |
| --- | --- | --- | --- |
| Current `master` / direct Xcode | iOS 12.0 or newer; Swift 5 language mode; iPhone and iPad target families | Hosted `macos-15` runs compiled the framework and executed the Swift math and UIKit iOS Simulator tests with Xcode 16.4 | Maintained repository path |
| Git-sourced CocoaPods from `master` or an exact commit | Root `SineWaveform.podspec` declares package version 0.0.6, iOS 12.0, Swift 5.0, and the current source glob | Ruby syntax and repository metadata are checked; the framework builds through the Xcode project, but CI does not execute `pod install` or `pod lib lint` | Source integration available, full CocoaPods integration unverified |
| Public CocoaPods trunk with `pod 'SineWaveform'` | No package entry was present in the official index when checked | No public-trunk installation was available to execute | Unavailable; do not document as an install path |
| Historical 2016 tags | Tag-specific podspecs and source from July 9, 2016 | No current CI or device verification | Historical snapshots only, not current compatibility claims |

Xcode 16.4 is evidence, not a maximum supported Xcode or SDK version. The
project does not declare an upper Xcode, Swift compiler, iOS SDK, simulator, or
device OS bound. Newer-toolchain compatibility must be established by a green
framework build and test run rather than inferred from this table.

## Current Source and Xcode

The Xcode project and root podspec agree on an iOS 12.0 deployment floor and
Swift 5 language mode. The shared scheme builds the framework for a generic iOS
Simulator, while the hosted tests execute shared waveform math and real UIKit
rendering. The project targets both iPhone and iPad device families.

This evidence covers compilation and simulator behavior only. It does not prove
physical-device execution, Interface Builder rendering across Xcode versions,
binary compatibility with a particular Swift toolchain, App Store submission,
or every iOS 12-through-current runtime combination.

## Git-sourced CocoaPods

The README's Git-sourced CocoaPods example reads the root podspec from the
selected repository revision. For reproducible builds, replace the mutable
`master` branch with an exact reviewed commit after verifying that commit in the
consumer application:

```ruby
pod 'SineWaveform', :git => 'https://github.com/garethpaul/sinewaveform.git', :commit => '<reviewed-commit-sha>'
```

The repository validates podspec Ruby syntax and metadata but does not install
CocoaPods in CI. Before calling a revision CocoaPods-compatible, run at least
`pod install` in a minimal iOS 12-or-newer consumer and `pod lib lint
SineWaveform.podspec` with the intended CocoaPods, Ruby, Xcode, and SDK versions.
Keep the generated Pods directory and consumer build artifacts out of this
repository.

## Public CocoaPods Trunk

`SineWaveform` was not published in the public CocoaPods Specs CDN when checked
on June 25, 2026. The official package list at
<https://cdn.cocoapods.org/all_pods.txt> contained no `SineWaveform` entry, and
<https://cocoapods.org/pods/SineWaveform> returned HTTP 404. Therefore plain
`pod 'SineWaveform'` installation is not a supported or verified route.

Recheck the official index before repeating that claim in the future. A later
publication requires a separately reviewed version bump, immutable matching
tag, trunk ownership, `pod lib lint`, clean consumer installation, release
notes, and hosted verification; updating this document alone is not a release.

## Historical 2016 Tags

All repository tags from 0.0.2 through 0.1.0 point to commits dated July 9,
2016. They are not equivalent to the current default branch:

- The 0.0.6 tag declares iOS 8.0 and has no `swift_version` declaration.
- The 0.1.0 tag contains podspec version 0.0.1, so the tag name and internal
  package version do not match.
- Older tag podspecs also contain historical transport URLs or metadata that
  the current root and archived reference podspecs have since corrected.

Do not infer iOS 12, Swift 5, current drawing guards, or current hosted-test
coverage from those tags. Consumers that intentionally reproduce a historical
tag own its legacy toolchain and security assessment.

## Unverified Boundaries

The repository does not currently claim:

- a public CocoaPods trunk release;
- a completed `pod install` or `pod lib lint` result for current `master`;
- physical iPhone or iPad execution;
- support below iOS 12 for current source;
- a maximum compatible Xcode, Swift compiler, SDK, simulator, or device OS;
- compatibility for the historical tags on modern toolchains; or
- semantic-version stability beyond the existing public Swift API.

To promote one of these boundaries, record the exact commit or tag, Xcode and
Swift versions, CocoaPods and Ruby versions where relevant, destination runtime,
commands, results, and cleanup in a focused plan and `CHANGES.md` entry.
