#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SWIFTC=${SWIFTC:-swiftc}
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/sinewaveform-tests.XXXXXX")

cleanup() {
    rm -rf -- "$BUILD_DIR"
}
trap cleanup 0
trap 'exit 129' 1
trap 'exit 130' 2
trap 'exit 143' 15

"$SWIFTC" \
    "$ROOT/SineWaveform/WaveformMath.swift" \
    "$ROOT/Tests/WaveformMathTests/main.swift" \
    -o "$BUILD_DIR/waveform-math-tests"

"$BUILD_DIR/waveform-math-tests"
