# Versioned Podspec Metadata

## Status: Completed

## Context

The root `SineWaveform.podspec` had already been updated to HTTPS metadata and
the lowercase GitHub source URL, but the archived `0.0.4` and `0.0.6`
podspec snapshots still used HTTP profile/homepage URLs and the old mixed-case
source repository URL.

## Objectives

- Keep archived podspec metadata aligned with the root package metadata.
- Use HTTPS for homepage and social metadata URLs.
- Use the lowercase GitHub source URL consistently.
- Extend static package checks across the archived podspec files.

## Work Completed

- Updated `SineWaveform/0.0.4/SineWaveform.podspec`.
- Updated `SineWaveform/0.0.6/SineWaveform.podspec`.
- Extended `scripts/check-sinewaveform-source.py` to scan all tracked podspecs
  for HTTP metadata and mixed-case source URLs.
- Updated README, VISION, and CHANGES.

## Verification

- `ruby -c SineWaveform.podspec`
- `ruby -c SineWaveform/0.0.4/SineWaveform.podspec`
- `ruby -c SineWaveform/0.0.6/SineWaveform.podspec`
- `python3 scripts/check-sinewaveform-source.py --mode package`
- `python3 scripts/check-sinewaveform-source.py --mode waveform`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Decide whether archived version directories should remain in the package
  source tree or move into release documentation.
- Add `pod spec lint` notes for a machine with a compatible CocoaPods/Xcode
  setup.
