# Main-Thread Waveform Updates Implementation Plan

Status: Completed

## Goal

Keep all `SiriWaveformView` state mutation and redraw invalidation on UIKit's
main thread without changing main-thread API behavior.

## Steps

1. Add background-call UIKit regression coverage.
2. Require an explicit main-thread guard and weak handoff.
3. Demonstrate RED against the current direct mutation.
4. Add the minimal main-queue dispatch path.
5. Run portable gates and hosted UIKit validation.

## Acceptance Criteria

- Background calls return before amplitude changes.
- Their queued update applies on the main queue.
- Main-thread calls remain synchronous.
- Removing the guard or dispatch fails portable verification.
- `make check`, `make lint`, `make test`, and `make build` pass.

## Verification Evidence

- RED: waveform checks rejected the absent main-thread guard, main-queue
  dispatch, and bounded update-path reuse.
- Clean Ruby 3.3 Make gates, six contract-checker tests, and the Swift 5.10
  waveform harness with 15 assertions plus its negative control passed.
- Hosted Check run `28215127189` passed the UIKit regression and framework
  build in Xcode 16.4; CodeQL run `28215125327` passed all configured languages.
- Codex review attempts on `21e08c3` and `855b64e` returned OpenAI API HTTP 401
  and were skipped per maintenance policy; manual exact-diff review was clean.
