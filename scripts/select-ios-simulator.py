#!/usr/bin/env python3
import json
import sys


devices_by_runtime = json.load(sys.stdin).get("devices", {})
for runtime in sorted(devices_by_runtime, reverse=True):
    if ".iOS-" not in runtime:
        continue
    for device in devices_by_runtime[runtime]:
        if device.get("isAvailable") and device.get("name", "").startswith("iPhone"):
            print(device["udid"])
            raise SystemExit(0)

print("no available iPhone Simulator found", file=sys.stderr)
raise SystemExit(1)
