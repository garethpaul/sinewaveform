# Make Authority Isolation

## Status: Completed

## Context

The verification entry point accepted caller-selected Python, Ruby, Swift, and
Xcode commands and derived its repository root with a whitespace-sensitive GNU
Make expression. A hostile `PATH`, command-line variable, environment variable,
or spaced checkout path could redirect or break checks before they inspected the
intended source tree.

## Work Completed

- Derived the repository root from the loaded Makefile with quoting that
  preserves spaces, quotes, and backticks for absolute external invocation,
  plus literal dollar syntax when Make is launched from inside the checkout.
- Added repository-owned launchers that select approved absolute system tools.
- Made shell flags, quality tools, temporary paths, and derived-data paths
  authoritative over caller assignments.
- Added a bounded hostile-input matrix across all seven public Make targets.
- Documented that GNU Make preload and additional `-f` files can execute during
  startup before an in-Makefile guard can establish authority.
- Documented that GNU Make also expands literal `$()` syntax in an absolute
  `-f` filename before exposing `MAKEFILE_LIST`, so that external filename form
  cannot be recovered portably by the loaded Makefile.

## Verification

- `make root-test` passed 133 target/authority cases, one literal-dollar checkout
  case, two metadata rejection cases, and three documented startup-boundary
  cases.
- Repository and external-directory `make check` passed.
- Hostile `PATH` and direct tool-variable probes could not replace verification
  tools.
- `git diff --check`, strict object validation, and secret screening passed.

## Scope Boundary

This change does not alter waveform rendering, public APIs, package metadata,
deployment targets, or signing behavior.

## Trust Boundary

The checked-in Makefile cannot make an already-started GNU Make process safe
against caller-supplied programs. `MAKEFILES` preloads and additional `-f`
programs can execute during GNU Make startup before this Makefile can reject
their visible metadata. Trusted automation must invoke the repository Makefile
without preload or additional Makefile programs.
