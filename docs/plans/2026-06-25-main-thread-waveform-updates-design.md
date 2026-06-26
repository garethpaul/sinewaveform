# Main-Thread Waveform Updates Design

Status: Completed

## Problem

`updateWithLevel(_:)` mutates waveform state and calls the inherited
`UIView.setNeedsDisplay()` method on whichever thread invokes the public API.
Audio levels are commonly produced away from the main queue, while Apple's
UIKit documentation requires view manipulation on the main thread.

## Options

1. Document a caller precondition. This leaves existing callers able to violate
   UIKit ownership and turns a reusable view into a crash-prone API.
2. Assert the main thread. This detects misuse but does not make the component
   safe for background level producers.
3. Handoff background calls to the main queue and preserve synchronous updates
   for main-thread callers.

## Decision

Use option 3. A background invocation returns after enqueuing a weakly captured
main-queue update. The existing normalization, phase, amplitude, and redraw
logic remains unchanged on the main thread.

## Verification

- Add a UIKit test that blocks the main thread until the background call
  returns, proves amplitude is unchanged, then proves the queued update applies.
- Add static and hostile-mutation contracts for the thread guard and handoff.
- Run `make check` plus focused lint, test, and build aliases.
