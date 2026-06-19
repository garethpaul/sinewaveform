---
title: Enforce Waveform Test Binary Execution
type: fix
date: 2026-06-19
---

# Enforce Waveform Test Binary Execution

Status: Completed

## Context

The waveform test-runner contract required the compiled binary path to appear
somewhere in `scripts/run-waveform-math-tests.sh`, but the same path appears in
both the compiler output argument and the standalone execution command. A
mutation that replaced the execution command therefore passed `make check` on
hosts without `swiftc`, even though hosted macOS CI would later catch the
missing behavior test execution.

## Requirements

- R1. Preserve the existing Swift compiler invocation and temporary build
  directory cleanup.
- R2. Require the compiler output to target the expected waveform test binary.
- R3. Require exactly one standalone command that executes the compiled test
  binary.
- R4. Keep the package contract effective when `swiftc` is unavailable.
- R5. Preserve the current executable Swift behavior tests and hosted iOS
  Simulator build.

## Work Completed

- Added a distinct package contract for the compiler output argument.
- Added a line-oriented contract requiring exactly one standalone execution of
  the compiled waveform test binary.
- Indexed the new maintenance evidence in README and change-log guidance.

## Verification

- The missing-execution mutation passed `make check` before the contract fix.
- The same mutation is rejected after the fix on a host without `swiftc`.
- `python3 scripts/check-sinewaveform-source.py --mode package` passed.
- `python3 scripts/check-sinewaveform-source.py --mode waveform` passed.
- Digest-pinned Swift executable tests passed from repository and external
  working directories.
- Repository and external-directory `make check` passed.
- Exact-head hosted `build` and `contract` checks remain required after push.
