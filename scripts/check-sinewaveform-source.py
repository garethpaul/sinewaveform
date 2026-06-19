#!/usr/bin/env python3
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-sinewaveform-baseline.md"
PHASE_PLAN = DOCS_PLANS / "2026-06-09-phase-accumulator-bound.md"
FINITE_INPUT_PLAN = DOCS_PLANS / "2026-06-10-finite-inspectable-inputs-and-ci.md"
FINITE_BOUNDS_PLAN = DOCS_PLANS / "2026-06-12-finite-waveform-bounds.md"
SAMPLE_BUDGET_PLAN = DOCS_PLANS / "2026-06-13-waveform-sample-budget.md"
ROOT_OVERRIDE_PLAN = DOCS_PLANS / "2026-06-14-make-root-override-protection.md"
EXACT_SAMPLE_BUDGET_PLAN = DOCS_PLANS / "2026-06-14-exact-waveform-sample-budget.md"
SUBNORMAL_WIDTH_PLAN = DOCS_PLANS / "2026-06-17-subnormal-width-geometry.md"
BEHAVIOR_TEST_PLAN = DOCS_PLANS / "2026-06-16-executable-waveform-math-tests.md"
TEMP_XCODE_ARTIFACT_PLAN = DOCS_PLANS / "2026-06-19-temp-xcode-artifacts.md"
TEST_EXECUTION_CONTRACT_PLAN = DOCS_PLANS / "2026-06-19-waveform-test-execution-contract.md"
WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"

EXPECTED_WORKFLOW = """name: Check

on:
  pull_request:
  push:
    branches:
      - master
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  contract:
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false
      - name: Set up Python
        uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6.2.0
        with:
          python-version: "3.12"
      - name: Run static verification
        run: make check

  build:
    runs-on: macos-15
    timeout-minutes: 15
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false
      - name: Show Xcode version
        run: xcodebuild -version
      - name: Run executable tests and build iOS Simulator framework
        run: make check
"""


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require_paths():
    errors = []
    for relative_path in (
        "SineWaveform.podspec",
        "SineWaveform/0.0.4/SineWaveform.podspec",
        "SineWaveform/0.0.6/SineWaveform.podspec",
        "SineWaveform/SineWaveForm.swift",
        "SineWaveform/WaveformMath.swift",
        "SineWaveform/SineWaveform.h",
        "SineWaveform.xcodeproj/project.pbxproj",
        "Tests/WaveformMathTests/main.swift",
        "scripts/run-waveform-math-tests.sh",
        "README.md",
        "docs/readme-overview.svg",
        "docs/device-preview.svg",
        "LICENSE",
    ):
        if not (ROOT / relative_path).exists():
            errors.append(f"missing required file: {relative_path}")
    return errors


def docs_plan_checks():
    errors = []
    if not CANONICAL_PLAN.exists():
        errors.append("docs/plans/2026-06-08-sinewaveform-baseline.md is missing")
    if not PHASE_PLAN.exists():
        errors.append("docs/plans/2026-06-09-phase-accumulator-bound.md is missing")
    if not FINITE_INPUT_PLAN.exists():
        errors.append("docs/plans/2026-06-10-finite-inspectable-inputs-and-ci.md is missing")
    if not FINITE_BOUNDS_PLAN.exists():
        errors.append("docs/plans/2026-06-12-finite-waveform-bounds.md is missing")
    if not SAMPLE_BUDGET_PLAN.exists():
        errors.append("docs/plans/2026-06-13-waveform-sample-budget.md is missing")
    if not ROOT_OVERRIDE_PLAN.exists():
        errors.append("docs/plans/2026-06-14-make-root-override-protection.md is missing")
    if not EXACT_SAMPLE_BUDGET_PLAN.exists():
        errors.append("docs/plans/2026-06-14-exact-waveform-sample-budget.md is missing")
    if not SUBNORMAL_WIDTH_PLAN.exists():
        errors.append("docs/plans/2026-06-17-subnormal-width-geometry.md is missing")
    if not BEHAVIOR_TEST_PLAN.exists():
        errors.append("docs/plans/2026-06-16-executable-waveform-math-tests.md is missing")
    if not TEMP_XCODE_ARTIFACT_PLAN.exists():
        errors.append("docs/plans/2026-06-19-temp-xcode-artifacts.md is missing")
    if not TEST_EXECUTION_CONTRACT_PLAN.exists():
        errors.append("docs/plans/2026-06-19-waveform-test-execution-contract.md is missing")

    plans = sorted(DOCS_PLANS.glob("*.md")) if DOCS_PLANS.exists() else []
    if not plans:
        errors.append("docs/plans must contain at least one completed plan")

    for plan_path in plans:
        plan = plan_path.read_text(encoding="utf-8")
        if "Status: Completed" not in plan or "make check" not in plan:
            errors.append(f"{plan_path.relative_to(ROOT)} must record completed status and make check verification")

    return errors


def package_checks():
    errors = docs_plan_checks() + require_paths()
    if errors:
        return errors

    podspec_paths = (
        "SineWaveform.podspec",
        "SineWaveform/0.0.4/SineWaveform.podspec",
        "SineWaveform/0.0.6/SineWaveform.podspec",
    )
    podspec = read_text("SineWaveform.podspec")
    for fragment in (
        's.name         = "SineWaveform"',
        's.version      = "0.0.6"',
        's.license = { :type => "MIT", :file => "LICENSE" }',
        's.source_files = "SineWaveform/*.{h,m,swift}"',
        's.platform     = :ios, "12.0"',
        's.swift_version = "5.0"',
    ):
        if fragment not in podspec:
            errors.append(f"podspec is missing expected metadata: {fragment}")
    if 's.platform     = :ios, "8.0"' in podspec:
        errors.append("root podspec must not advertise the retired iOS 8 deployment target")

    for podspec_path in podspec_paths:
        podspec_source = read_text(podspec_path)
        if re.search(r's\.homepage\s*=\s*"http://', podspec_source):
            errors.append(f"{podspec_path} homepage must use HTTPS")
        if re.search(r's\.social_media_url\s*=\s*"http://', podspec_source):
            errors.append(f"{podspec_path} social_media_url must use HTTPS")
        if "https://github.com/garethpaul/SineWaveform.git" in podspec_source:
            errors.append(f"{podspec_path} source URL must match the lowercase GitHub repo URL")
        if re.search(r's\.description\s*=\s*""', podspec_source):
            errors.append(f"{podspec_path} must not assign an empty podspec description before the real description")

    project = read_text("SineWaveform.xcodeproj/project.pbxproj")
    if "productName = SineWaveform;" not in project:
        errors.append("Xcode project must expose the SineWaveform target")
    for fragment in ("IPHONEOS_DEPLOYMENT_TARGET = 12.0;", "SWIFT_VERSION = 5.0;"):
        if fragment not in project:
            errors.append(f"Xcode project must keep current build setting: {fragment}")
    for fragment in ("WaveformMath.swift", "WaveformMath.swift in Sources"):
        if fragment not in project:
            errors.append(f"Xcode project must compile shared waveform math: {fragment}")

    readme = read_text("README.md")
    for fragment in (
        "<!-- README-OVERVIEW-IMAGE -->",
        "![Project overview](docs/readme-overview.svg)",
        "## Device Preview",
        "<!-- DEVICE-PREVIEW-IMAGE -->",
        "![Device preview](docs/device-preview.svg)",
    ):
        if fragment not in readme:
            errors.append(f"README must keep visual documentation contract: {fragment}")

    for relative_path in ("docs/readme-overview.svg", "docs/device-preview.svg"):
        try:
            ET.parse(ROOT / relative_path)
        except ET.ParseError as error:
            errors.append(f"{relative_path} must be valid XML: {error}")

    workflow = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.exists() else ""
    for fragment in (
        "permissions:",
        "contents: read",
        "concurrency:",
        "cancel-in-progress: true",
        "contract:",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 5",
        "build:",
        "runs-on: macos-15",
        "timeout-minutes: 15",
        "workflow_dispatch:",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        "persist-credentials: false",
        'python-version: "3.12"',
        "run: make check",
    ):
        if fragment not in workflow:
            errors.append(f"GitHub Actions workflow must keep contract: {fragment}")

    workflow_files = sorted(
        path
        for path in WORKFLOW.parent.glob("*")
        if path.is_file() and path.suffix in {".yml", ".yaml"}
    )
    if workflow_files != [WORKFLOW]:
        errors.append(".github/workflows/check.yml must remain the only approved workflow")
    if workflow != EXPECTED_WORKFLOW:
        errors.append(".github/workflows/check.yml must match the approved build policy")

    checker_source = Path(__file__).read_text(encoding="utf-8")
    for fragment in (
        "while true",
        "let sampleX = WaveformMath.sampleX(",
        "if sampleX == width { break }",
    ):
        if checker_source.count(f'"{fragment}"') < 2:
            errors.append(f"waveform checker must retain right-edge assertion: {fragment}")

    makefile = read_text("Makefile")
    root_declaration = "override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))"
    if makefile.count(root_declaration) != 1:
        errors.append("Makefile must contain exactly one protected repository-root declaration")
    tool_and_root_block = "\n".join((
        "PYTHON ?= python3",
        "RUBY ?= ruby",
        "SWIFTC ?= swiftc",
        "XCODEBUILD ?= xcodebuild",
        "TMPDIR ?= /tmp",
        "XCODEBUILD_DERIVED_DATA_PATH ?= $(abspath $(TMPDIR)/sinewaveform-derived-data)",
        root_declaration,
    ))
    if makefile.count(tool_and_root_block) != 1:
        errors.append("Makefile must keep tool and temp-artifact overrides before the protected repository root")

    for fragment in (
        ".PHONY: build check lint test verify",
        "build: lint",
        "verify: lint test build",
        "check: verify",
        '"$(ROOT)/SineWaveform.podspec"',
        '"$(ROOT)/scripts/check-sinewaveform-source.py"',
        '"$(ROOT)/scripts/run-waveform-math-tests.sh"',
        '"$(ROOT)/SineWaveform.xcodeproj"',
        "-scheme SineWaveform",
        '-derivedDataPath "$(XCODEBUILD_DERIVED_DATA_PATH)"',
        "generic/platform=iOS Simulator",
        "CODE_SIGNING_ALLOWED=NO",
    ):
        if fragment not in makefile:
            errors.append(f"Makefile must keep root-independent build contract: {fragment}")

    if "docs/plans/2026-06-14-make-root-override-protection.md" not in read_text("README.md"):
        errors.append("README must index Make root override protection evidence")
    if "docs/plans/2026-06-14-exact-waveform-sample-budget.md" not in read_text("README.md"):
        errors.append("README must index exact waveform sample budget evidence")
    if "docs/plans/2026-06-16-executable-waveform-math-tests.md" not in read_text("README.md"):
        errors.append("README must index executable waveform math test evidence")
    if str(SUBNORMAL_WIDTH_PLAN.relative_to(ROOT)) not in read_text("README.md"):
        errors.append("README must index subnormal-width geometry evidence")
    if str(TEMP_XCODE_ARTIFACT_PLAN.relative_to(ROOT)) not in read_text("README.md"):
        errors.append("README must index temp Xcode artifact evidence")
    if str(TEST_EXECUTION_CONTRACT_PLAN.relative_to(ROOT)) not in read_text("README.md"):
        errors.append("README must index waveform test execution contract evidence")

    for doc_path in ("README.md", "VISION.md", "SECURITY.md", "CHANGES.md"):
        document = re.sub(r"\s+", " ", read_text(doc_path)).lower()
        if "waveform sample budget" not in document:
            errors.append(f"{doc_path} must document the waveform sample budget")
        if "exact 4,096-point waveform sample budget" not in document:
            errors.append(f"{doc_path} must document the exact endpoint-inclusive sample budget")
        if "subnormal waveform widths are rejected before core graphics mutation" not in document:
            errors.append(f"{doc_path} must document subnormal-width rejection")

    return errors


def waveform_checks():
    errors = require_paths()
    if errors:
        return errors

    source = read_text("SineWaveform/SineWaveForm.swift")
    math_source = read_text("SineWaveform/WaveformMath.swift")
    test_source = read_text("Tests/WaveformMathTests/main.swift")
    test_runner = read_text("scripts/run-waveform-math-tests.sh")
    if "class SiriWaveformView: UIView" not in source:
        errors.append("SiriWaveformView class is missing")
    if "for waveNumber in 0...numOfWaves" in source:
        errors.append("drawRect must not divide by raw numOfWaves")
    if "for waveNumber in 0...waveCount" in source:
        errors.append("drawRect must not draw one more wave than the clamped wave count")
    if "x += density" in source:
        errors.append("drawRect must not advance by raw density")
    if "while x < width + step" in source:
        errors.append("drawRect must not sample beyond the right view bound")
    if "let waveCount = max(1, numOfWaves)" in source:
        errors.append("drawRect must not leave numOfWaves without an upper bound")
    if "private let maximumWaveCount = 32" not in source:
        errors.append("SiriWaveformView must define a maximum draw-time wave count")
    if "let waveCount = min(max(1, numOfWaves), maximumWaveCount)" not in source:
        errors.append("drawRect must clamp wave count to a bounded 1...maximumWaveCount range")
    if "let step = normalizedValue(density, minimum: 1.0, maximum: maximumDensity, fallback: 4.0)" not in source:
        errors.append("drawRect must clamp draw step through finite input normalization")
    for fragment in (
        "while true",
        "let sampleX = WaveformMath.sampleX(",
        "WaveformMath.waveformScaling(sampleX: sampleX, midpoint: midpoint)",
        "sampleX / width",
        "CGPoint(x: sampleX, y: y)",
        "if sampleX == width { break }",
    ):
        if fragment not in source:
            errors.append(f"drawRect right-edge sampling contract is missing: {fragment}")
    if "guard let context = UIGraphicsGetCurrentContext() else { return }" not in source:
        errors.append("drawRect must guard graphics context availability")
    finite_bounds_guard = "guard width.isFinite && height.isFinite && width > 0.0 && height > 0.0 else { return }"
    if finite_bounds_guard not in source:
        errors.append("drawRect must skip non-finite and non-positive bounds before division")
    elif source.index(finite_bounds_guard) > source.index("context.clear(bounds)"):
        errors.append("drawRect must validate finite bounds before mutating the graphics context")
    if "for waveNumber in 0..<waveCount" not in source:
        errors.append("drawRect must iterate within the clamped wave count")
    if source.count("UIGraphicsGetCurrentContext()") != 1:
        errors.append("drawRect must fetch the graphics context once before the wave loop")
    if "let maxAmplitude = halfHeight - 4.0" in source:
        errors.append("drawRect must not allow negative max amplitude for short bounds")
    if "let maxAmplitude = max(halfHeight - 4.0, 0.0)" not in source:
        errors.append("drawRect must clamp max amplitude to a nonnegative value")
    if "context.setLineWidth(waveNumber == 0 ? primaryWaveLineWidth : secondaryWaveLineWidth)" in source:
        errors.append("drawRect must not pass raw inspectable line widths to Core Graphics")
    if "let primaryLineWidth = normalizedValue(primaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 2.0)" not in source:
        errors.append("drawRect must clamp the primary line width through finite input normalization")
    if "let secondaryLineWidth = normalizedValue(secondaryWaveLineWidth, minimum: 0.0, maximum: maximumLineWidth, fallback: 3.0)" not in source:
        errors.append("drawRect must clamp the secondary line width through finite input normalization")
    if "context.setLineWidth(waveNumber == 0 ? primaryLineWidth : secondaryLineWidth)" not in source:
        errors.append("drawRect must set Core Graphics line width from clamped values")
    if "_amplitude = fmax(level, idleAmplitude)" in source:
        errors.append("updateWithLevel must not assign unbounded caller-provided amplitude")
    if "let normalizedLevel = min(max(level, 0.0), 1.0)" in source:
        errors.append("updateWithLevel must not normalize caller-provided levels inline")
    if "let normalizedIdleAmplitude = min(max(idleAmplitude, 0.0), 1.0)" in source:
        errors.append("updateWithLevel must not normalize idleAmplitude inline")
    if "private func normalizedUnitValue(_ value: CGFloat) -> CGFloat" not in source:
        errors.append("SiriWaveformView must centralize unit-interval value normalization")
    if "return WaveformMath.normalizedUnitValue(value)" not in source:
        errors.append("unit-interval normalization must use shared finite input normalization")
    if "let normalizedLevel = normalizedUnitValue(level)" not in source:
        errors.append("updateWithLevel must normalize caller-provided levels through the shared helper")
    if "let normalizedIdleAmplitude = normalizedValue(idleAmplitude, minimum: 0.0, maximum: 1.0, fallback: 0.01)" not in source:
        errors.append("updateWithLevel must normalize idleAmplitude with its inspectable default fallback")
    if "_amplitude = max(normalizedLevel, normalizedIdleAmplitude)" not in source:
        errors.append("updateWithLevel must use the clamped level and idle amplitude")
    if "_phase += phaseShift" in source:
        errors.append("updateWithLevel must not let phase grow without bound")
    if "private let phaseCycle = CGFloat(2.0 * pi)" not in source:
        errors.append("SiriWaveformView must define a single-cycle phase bound")
    if "_phase = normalizedPhase(_phase + safePhaseShift)" not in source:
        errors.append("updateWithLevel must normalize phase after applying the bounded phase shift")
    if "private func normalizedPhase(_ phase: CGFloat) -> CGFloat" not in source:
        errors.append("SiriWaveformView must centralize phase normalization")
    if "return WaveformMath.normalizedPhase(phase, cycle: phaseCycle)" not in source:
        errors.append("phase normalization must delegate to shared executable math")
    if "phase.truncatingRemainder(dividingBy: cycle)" not in math_source:
        errors.append("shared phase normalization must wrap within one cycle")
    if "wrappedPhase >= 0.0 ? wrappedPhase : wrappedPhase + cycle" not in math_source:
        errors.append("phase normalization must shift negative wrapped phases back into the positive cycle")
    for fragment in (
        "private let maximumFrequency: CGFloat = 100.0",
        "private let maximumDensity: CGFloat = 100.0",
        "private let maximumLineWidth: CGFloat = 100.0",
        "private func normalizedValue(_ value: CGFloat, minimum: CGFloat, maximum: CGFloat, fallback: CGFloat) -> CGFloat",
        "return WaveformMath.normalizedValue(value, minimum: minimum, maximum: maximum, fallback: fallback)",
        "let safePhaseShift = normalizedValue(phaseShift, minimum: -phaseCycle, maximum: phaseCycle, fallback: -0.15)",
        "let drawFrequency = normalizedValue(frequency, minimum: -maximumFrequency, maximum: maximumFrequency, fallback: 1.5)",
        "private let maximumSamplePointCount = 4096",
        "let maximumSampleIntervalCount = maximumSamplePointCount - 1",
        "let sampleStep = WaveformMath.sampleStep(",
        "var sampleIndex = 0",
        "let sampleX = WaveformMath.sampleX(",
        "sampleIndex += 1",
        "x += sampleStep",
        "* drawFrequency + _phase",
    ):
        if fragment not in source:
            errors.append(f"waveform finite-input contract is missing: {fragment}")
    for fragment in (
        "static func waveformScaling(sampleX: CGFloat, midpoint: CGFloat) -> CGFloat",
        "let normalizedX = (sampleX - midpoint) / midpoint",
        "return -(normalizedX * normalizedX) + 1.0",
        "let midpoint = width / 2.0",
        "guard midpoint > 0.0 else { return }",
        "WaveformMath.waveformScaling(sampleX: sampleX, midpoint: midpoint)",
        "WaveformMath.waveformScaling(sampleX: 0.0, midpoint: .leastNonzeroMagnitude)",
    ):
        if fragment not in math_source + source + test_source:
            errors.append(f"waveform subnormal-width contract is missing: {fragment}")
    midpoint_guard = source.find("guard midpoint > 0.0 else { return }")
    context_clear = source.find("context.clear(bounds)")
    if min(midpoint_guard, context_clear) < 0 or midpoint_guard > context_clear:
        errors.append("drawRect must reject midpoint underflow before graphics context mutation")
    if (
        "1 / mid * (sampleX - mid)" in source
        or "1 / midpoint * (sampleX - midpoint)" in source
        or "1 / midpoint * (sampleX - midpoint)" in math_source
    ):
        errors.append("waveform scaling must not use an overflowing reciprocal")
    for fragment in (
        "guard value == value else { return fallback }",
        "return min(max(value, minimum), maximum)",
        "return max(step, width / CGFloat(maximumSampleIntervalCount))",
        "return index == maximumSampleIntervalCount ? width : min(accumulatedX, width)",
    ):
        if fragment not in math_source:
            errors.append(f"shared executable waveform math is missing: {fragment}")
    for fragment in (
        "if !actual.isFinite || abs(actual - expected) > accuracy",
        "WaveformMath.normalizedValue(.nan",
        "WaveformMath.normalizedPhase(-0.5",
        "WaveformMath.sampleStep(width: 8190.0",
        "WaveformMath.sampleX(index: 4095",
    ):
        if fragment not in test_source:
            errors.append(f"executable waveform behavior coverage is missing: {fragment}")
    for fragment in (
        '"$SWIFTC"',
        '"$ROOT/SineWaveform/WaveformMath.swift"',
        '"$ROOT/Tests/WaveformMathTests/main.swift"',
        '"$BUILD_DIR/waveform-math-tests"',
    ):
        if fragment not in test_runner:
            errors.append(f"waveform behavior test runner is missing: {fragment}")
    executable = '"$BUILD_DIR/waveform-math-tests"'
    if f'-o {executable}' not in test_runner:
        errors.append("waveform behavior test runner must compile the expected test binary")
    if [line.strip() for line in test_runner.splitlines()].count(executable) != 1:
        errors.append("waveform behavior test runner must execute the compiled test binary exactly once")
    if "width / CGFloat(maximumSamplePointCount)" in source or "maximumSampleCount" in source:
        errors.append("waveform sample budgeting must count both endpoint samples")
    if EXACT_SAMPLE_BUDGET_PLAN.exists():
        plan = EXACT_SAMPLE_BUDGET_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "hostile exact sample-budget mutations were rejected",
        ):
            if evidence not in plan:
                errors.append(f"{EXACT_SAMPLE_BUDGET_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}")
    if SUBNORMAL_WIDTH_PLAN.exists():
        plan = SUBNORMAL_WIDTH_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "repository and external-directory `make check` passed",
            "hostile subnormal-width mutations were rejected",
            "generated-artifact and credential-pattern audits passed",
        ):
            if evidence not in plan:
                errors.append(f"{SUBNORMAL_WIDTH_PLAN.relative_to(ROOT)} must record verification evidence {evidence!r}")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("package", "waveform"), required=True)
    args = parser.parse_args()

    errors = package_checks() if args.mode == "package" else waveform_checks()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"{args.mode} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
