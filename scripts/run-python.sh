#!/bin/sh
set -eu

if [ "${1:-}" = -m ]; then
    exec /usr/bin/python3 -I -B "$@"
fi

exec /usr/bin/python3 -I -B -c 'import os, runpy, sys; script = sys.argv[1]; sys.argv = sys.argv[1:]; sys.path.insert(0, os.path.dirname(os.path.realpath(script))); runpy.run_path(script, run_name="__main__")' "$@"
