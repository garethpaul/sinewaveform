#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-sinewaveform-baseline.md"
PHASE_PLAN = DOCS_PLANS / "2026-06-09-phase-accumulator-bound.md"
FINITE_INPUT_PLAN = DOCS_PLANS / "2026-06-10-finite-inspectable-inputs-and-ci.md"
WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require_paths():
    errors = []
    for relative_path in (
        "SineWaveform.podspec",
        "SineWaveform/0.0.4/SineWaveform.podspec",
        "SineWaveform/0.0.6/SineWaveform.podspec",
        "SineWaveform/SineWaveForm.swift",
        "SineWaveform/SineWaveform.h",
        "SineWaveform.xcodeproj/project.pbxproj",
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
    ):
        if fragment not in podspec:
            errors.append(f"podspec is missing expected metadata: {fragment}")

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
        'python-version: "3.12"',
        "run: make check",
        "run: make build",
    ):
        if fragment not in workflow:
            errors.append(f"GitHub Actions workflow must keep contract: {fragment}")

    makefile = read_text("Makefile")
    for fragment in (
        "ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))",
        '"$(ROOT)/SineWaveform.podspec"',
        '"$(ROOT)/scripts/check-sinewaveform-source.py"',
        '"$(ROOT)/SineWaveform.xcodeproj"',
        "generic/platform=iOS Simulator",
        "CODE_SIGNING_ALLOWED=NO",
    ):
        if fragment not in makefile:
            errors.append(f"Makefile must keep root-independent build contract: {fragment}")

    return errors


def waveform_checks():
    errors = require_paths()
    if errors:
        return errors

    source = read_text("SineWaveform/SineWaveForm.swift")
    if "class SiriWaveformView: UIView" not in source:
        errors.append("SiriWaveformView class is missing")
    if "for waveNumber in 0...numOfWaves" in source:
        errors.append("drawRect must not divide by raw numOfWaves")
    if "for waveNumber in 0...waveCount" in source:
        errors.append("drawRect must not draw one more wave than the clamped wave count")
    if "x += density" in source:
        errors.append("drawRect must not advance by raw density")
    if "let waveCount = max(1, numOfWaves)" in source:
        errors.append("drawRect must not leave numOfWaves without an upper bound")
    if "private let maximumWaveCount = 32" not in source:
        errors.append("SiriWaveformView must define a maximum draw-time wave count")
    if "let waveCount = min(max(1, numOfWaves), maximumWaveCount)" not in source:
        errors.append("drawRect must clamp wave count to a bounded 1...maximumWaveCount range")
    if "let step = normalizedValue(density, minimum: 1.0, maximum: maximumDensity, fallback: 4.0)" not in source:
        errors.append("drawRect must clamp draw step through finite input normalization")
    if "guard let context = UIGraphicsGetCurrentContext() else { return }" not in source:
        errors.append("drawRect must guard graphics context availability")
    if "guard width > 0.0 && height > 0.0 else { return }" not in source:
        errors.append("drawRect must skip zero-size bounds before division")
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
    if "return normalizedValue(value, minimum: 0.0, maximum: 1.0, fallback: 0.0)" not in source:
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
    if "fmod(Double(phase), Double(phaseCycle))" not in source:
        errors.append("phase normalization must wrap with fmod")
    if "return CGFloat(fmod(Double(phase), Double(phaseCycle)))" in source:
        errors.append("phase normalization must not return negative fmod results directly")
    if "let wrappedPhase = CGFloat(fmod(Double(phase), Double(phaseCycle)))" not in source:
        errors.append("phase normalization must store the fmod result before range correction")
    if "wrappedPhase >= 0.0 ? wrappedPhase : wrappedPhase + phaseCycle" not in source:
        errors.append("phase normalization must shift negative wrapped phases back into the positive cycle")
    for fragment in (
        "private let maximumFrequency: CGFloat = 100.0",
        "private let maximumDensity: CGFloat = 100.0",
        "private let maximumLineWidth: CGFloat = 100.0",
        "private func normalizedValue(_ value: CGFloat, minimum: CGFloat, maximum: CGFloat, fallback: CGFloat) -> CGFloat",
        "guard value == value else { return fallback }",
        "return min(max(value, minimum), maximum)",
        "let safePhaseShift = normalizedValue(phaseShift, minimum: -phaseCycle, maximum: phaseCycle, fallback: -0.15)",
        "let drawFrequency = normalizedValue(frequency, minimum: -maximumFrequency, maximum: maximumFrequency, fallback: 1.5)",
        "* drawFrequency + _phase",
    ):
        if fragment not in source:
            errors.append(f"waveform finite-input contract is missing: {fragment}")

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
