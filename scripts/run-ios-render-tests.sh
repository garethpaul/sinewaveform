#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && /bin/pwd -P)
PYTHON="$ROOT/scripts/run-python.sh"
XCODEBUILD="$ROOT/scripts/run-xcodebuild.sh"
DERIVED_DATA_PATH=${XCODETEST_DERIVED_DATA_PATH:-/tmp/sinewaveform-render-tests-derived-data}

device_id=$(/usr/bin/xcrun simctl list devices available -j | "$PYTHON" "$ROOT/scripts/select-ios-simulator.py")
/usr/bin/xcrun simctl boot "$device_id" >/dev/null 2>&1 || true
/usr/bin/xcrun simctl bootstatus "$device_id" -b

exec "$XCODEBUILD" \
    -project "$ROOT/SineWaveform.xcodeproj" \
    -scheme SineWaveform \
    -destination "platform=iOS Simulator,id=$device_id" \
    -derivedDataPath "$DERIVED_DATA_PATH" \
    CODE_SIGNING_ALLOWED=NO \
    test
