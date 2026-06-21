#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON="$ROOT/scripts/run-python.sh"
SWIFTC="$ROOT/scripts/run-swiftc.sh"

exec "$PYTHON" "$ROOT/scripts/verify-waveform-math-execution.py" --swiftc "$SWIFTC"
