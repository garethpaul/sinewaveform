# Podspec Description Guard

## Status: Completed

## Context

`sinewaveform` keeps a root podspec and archived versioned podspecs. Each
podspec assigned `s.description = ""` immediately before assigning the real
heredoc description. The later assignment wins, but the empty placeholder makes
package metadata harder to audit and can return if podspecs are copied forward.

## Objectives

- Keep root and archived podspec metadata aligned.
- Remove empty placeholder description assignments.
- Extend static package checks to reject empty podspec descriptions.
- Preserve the existing HTTPS URL, source URL, license, source-file, waveform,
  and completed-plan checks.

## Work Completed

- Removed empty `s.description = ""` assignments from all tracked podspecs.
- Extended `scripts/check-sinewaveform-source.py --mode package` to reject
  empty podspec descriptions.
- Updated README, VISION, and CHANGES notes for the metadata guard.

## Verification

- `ruby -c SineWaveform.podspec`
- `python3 scripts/check-sinewaveform-source.py --mode package`
- `make check`
- `make verify`
- `git diff --check`
