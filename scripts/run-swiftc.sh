#!/bin/sh
set -eu

for compiler in /usr/bin/swiftc /usr/local/swift/usr/bin/swiftc; do
    if [ -x "$compiler" ]; then
        if [ "${1:-}" = --available ]; then
            exit 0
        fi
        exec "$compiler" "$@"
    fi
done

if [ "${1:-}" = --available ]; then
    exit 1
fi
printf '%s\n' 'swiftc not found in an approved system location' >&2
exit 127
