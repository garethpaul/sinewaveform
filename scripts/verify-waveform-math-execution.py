#!/usr/bin/env python3
import argparse
import os
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSERTION_IDS = (
    "nan-fallback",
    "positive-infinity",
    "negative-infinity",
    "unit-lower-bound",
    "unit-upper-bound",
    "positive-phase-wrap",
    "negative-phase-wrap",
    "wide-sample-step",
    "normal-sample-step",
    "interior-sample",
    "right-edge-sample",
    "overshoot-clamp",
    "left-edge-envelope",
    "center-envelope",
    "right-edge-envelope",
)


def run(binary, nonce, mode):
    return subprocess.run(
        [str(binary), nonce, mode],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def expected_pass_output(nonce):
    lines = [f"ASSERT {nonce} {identifier} PASS" for identifier in ASSERTION_IDS]
    lines.append(f"COMPLETE {nonce} {len(ASSERTION_IDS)}")
    return "\n".join(lines) + "\n"


def verify(swiftc):
    with tempfile.TemporaryDirectory(prefix="sinewaveform-execution-") as temporary:
        binary = Path(temporary) / "waveform-math-tests"
        subprocess.run(
            [
                swiftc,
                str(ROOT / "SineWaveform/WaveformMath.swift"),
                str(ROOT / "Tests/WaveformMathTests/main.swift"),
                "-o",
                str(binary),
            ],
            cwd=ROOT,
            timeout=60,
            check=True,
        )

        pass_nonce = os.urandom(32).hex()
        passing = run(binary, pass_nonce, "normal")
        expected_stdout = expected_pass_output(pass_nonce)
        if passing.returncode != 0 or passing.stdout != expected_stdout or passing.stderr:
            raise SystemExit(
                "waveform passing execution did not produce the required assertion trace "
                f"(status={passing.returncode}, stdout={passing.stdout!r}, stderr={passing.stderr!r})"
            )

        failure_nonce = os.urandom(32).hex()
        failing = run(binary, failure_nonce, "force-failure")
        expected_failure = (
            f"ASSERT {failure_nonce} nan-fallback FAIL: NaN uses the caller-provided fallback: "
            "expected 0.5, got 0.25\n"
        )
        expected_failure_stdout = "\n".join(
            f"ASSERT {failure_nonce} {identifier} PASS" for identifier in ASSERTION_IDS[1:]
        ) + "\n"
        if (
            failing.returncode != 1
            or failing.stdout != expected_failure_stdout
            or failing.stderr != expected_failure
        ):
            raise SystemExit(
                "waveform negative control was not independently observed as a real failure "
                f"(status={failing.returncode}, stdout={failing.stdout!r}, stderr={failing.stderr!r})"
            )

    print(f"WaveformMath execution verified: {len(ASSERTION_IDS)} assertions and negative control")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--swiftc", default="swiftc")
    arguments = parser.parse_args()
    verify(arguments.swiftc)


if __name__ == "__main__":
    main()
