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
