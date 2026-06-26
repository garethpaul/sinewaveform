# AGENTS.md

## Repository purpose

`garethpaul/sinewaveform` is a reusable Swift waveform view that produces a Siri-style animation for Apple platforms.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `SineWaveform.xcodeproj` - Xcode project
- `plans` - repository source or sample assets
- `screenshots` - repository source or sample assets
- `SineWaveform` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- Xcode build artifacts use `/tmp/sinewaveform-derived-data`; keep that
  repository-controlled location unless a security-focused change replaces it.
- Local Apple development: `open SineWaveform.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: C/C++ headers (1), Swift (3).
- Preserve Swift 5 language mode, the iOS 12 deployment target, and signing assumptions unless the change explicitly updates compatibility.

## Testing guidance

- Test-related files detected: `docs/plans/2026-06-08-podspec-description-guard.md`, `docs/plans/2026-06-08-versioned-podspec-metadata.md`, `SineWaveform.podspec`, `SineWaveform/0.0.4/SineWaveform.podspec`, `SineWaveform/0.0.6/SineWaveform.podspec`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- `make test` compiles and runs the shared waveform math harness when `swiftc`
  is available; the hosted macOS gate is the authoritative execution boundary.
- Keep the test-runner source contract sensitive to a missing, duplicated, or
  replaced standalone waveform test-binary execution command.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.
- Preserve the shared finite-range normalization path for inspectable waveform
  values before phase math or Core Graphics calls.
- Subnormal waveform widths are rejected before Core Graphics mutation.
- Preserve `isOpaque = false` in both UIKit initialization paths and keep a nil
  background transparent in the hosted simulator rendering tests.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-sinewaveform-baseline.md` for the canonical package and drawing safety baseline.
- See `docs/plans/2026-06-08-versioned-podspec-metadata.md` for the archived podspec metadata guard.
- Preserve the installation naming boundary: pod/module `SineWaveform`, public
  view `SiriWaveformView`, and historical source file `SineWaveForm.swift`.
- See `docs/plans/2026-06-25-installation-naming.md` for the checked install and
  import examples.
- See `docs/plans/2026-06-25-transparent-waveform-rendering.md` for the UIKit
  render-test boundary and transparent compositing contract.
- Keep `.github/workflows/check.yml` as the only workflow, with immutable actions, read-only permissions, and persisted checkout credentials disabled in both jobs.
- Preserve the checked-in project overview and device preview SVG references in README.md.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
