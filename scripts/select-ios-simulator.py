#!/usr/bin/env python3
import json
import sys


MINIMUM_IOS_VERSION = (12, 0)


def ios_version(runtime):
    marker = ".iOS-"
    if marker not in runtime:
        return None
    try:
        return tuple(int(component) for component in runtime.split(marker, 1)[1].split("-"))
    except ValueError:
        return None


devices_by_runtime = json.load(sys.stdin).get("devices", {})
ios_runtimes = []
for runtime, devices in devices_by_runtime.items():
    version = ios_version(runtime)
    if version is not None and version >= MINIMUM_IOS_VERSION:
        ios_runtimes.append((version, devices))

for _, devices in sorted(ios_runtimes, reverse=True):
    for device in devices:
        if device.get("isAvailable") and device.get("name", "").startswith("iPhone"):
            print(device["udid"])
            raise SystemExit(0)

print("no available iPhone Simulator found", file=sys.stderr)
raise SystemExit(1)
