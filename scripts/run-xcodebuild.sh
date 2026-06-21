#!/bin/sh
set -eu

if [ "${1:-}" = --available ]; then
    [ -x /usr/bin/xcodebuild ]
    exit
fi

exec /usr/bin/xcodebuild "$@"
