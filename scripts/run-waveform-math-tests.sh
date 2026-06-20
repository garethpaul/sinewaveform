#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON=${PYTHON:-python3}
SWIFTC=${SWIFTC:-swiftc}

exec "$PYTHON" "$ROOT/scripts/verify-waveform-math-execution.py" --swiftc "$SWIFTC"
