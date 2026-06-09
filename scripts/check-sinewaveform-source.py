#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-sinewaveform-baseline.md"
PHASE_PLAN = DOCS_PLANS / "2026-06-09-phase-accumulator-bound.md"


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
    if "let step = max(density, 1.0)" not in source:
        errors.append("drawRect must clamp draw step to a positive value")
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
    if "CGContextSetLineWidth(context, (waveNumber == 0 ? primaryWaveLineWidth : secondaryWaveLineWidth))" in source:
        errors.append("drawRect must not pass raw inspectable line widths to Core Graphics")
    if "let primaryLineWidth = max(primaryWaveLineWidth, 0.0)" not in source:
        errors.append("drawRect must clamp the primary line width to a nonnegative value")
    if "let secondaryLineWidth = max(secondaryWaveLineWidth, 0.0)" not in source:
        errors.append("drawRect must clamp the secondary line width to a nonnegative value")
    if "CGContextSetLineWidth(context, (waveNumber == 0 ? primaryLineWidth : secondaryLineWidth))" not in source:
        errors.append("drawRect must set Core Graphics line width from clamped values")
    if "_amplitude = fmax(level, idleAmplitude)" in source:
        errors.append("updateWithLevel must not assign unbounded caller-provided amplitude")
    if "let normalizedLevel = min(max(level, 0.0), 1.0)" in source:
        errors.append("updateWithLevel must not normalize caller-provided levels inline")
    if "let normalizedIdleAmplitude = min(max(idleAmplitude, 0.0), 1.0)" in source:
        errors.append("updateWithLevel must not normalize idleAmplitude inline")
    if "private func normalizedUnitValue(value: CGFloat) -> CGFloat" not in source:
        errors.append("SiriWaveformView must centralize unit-interval value normalization")
    if "guard value == value else { return 0.0 }" not in source:
        errors.append("unit-interval normalization must reject NaN values")
    if "return min(max(value, 0.0), 1.0)" not in source:
        errors.append("unit-interval normalization must clamp values into 0...1")
    if "let normalizedLevel = normalizedUnitValue(level)" not in source:
        errors.append("updateWithLevel must normalize caller-provided levels through the shared helper")
    if "let normalizedIdleAmplitude = normalizedUnitValue(idleAmplitude)" not in source:
        errors.append("updateWithLevel must normalize idleAmplitude through the shared helper")
    if "_amplitude = max(normalizedLevel, normalizedIdleAmplitude)" not in source:
        errors.append("updateWithLevel must use the clamped level and idle amplitude")
    if "_phase += phaseShift" in source:
        errors.append("updateWithLevel must not let phase grow without bound")
    if "private let phaseCycle = CGFloat(2.0 * pi)" not in source:
        errors.append("SiriWaveformView must define a single-cycle phase bound")
    if "_phase = normalizedPhase(_phase + phaseShift)" not in source:
        errors.append("updateWithLevel must normalize phase after applying phaseShift")
    if "private func normalizedPhase(phase: CGFloat) -> CGFloat" not in source:
        errors.append("SiriWaveformView must centralize phase normalization")
    if "fmod(Double(phase), Double(phaseCycle))" not in source:
        errors.append("phase normalization must wrap with fmod")
    if "return CGFloat(fmod(Double(phase), Double(phaseCycle)))" in source:
        errors.append("phase normalization must not return negative fmod results directly")
    if "let wrappedPhase = CGFloat(fmod(Double(phase), Double(phaseCycle)))" not in source:
        errors.append("phase normalization must store the fmod result before range correction")
    if "wrappedPhase >= 0.0 ? wrappedPhase : wrappedPhase + phaseCycle" not in source:
        errors.append("phase normalization must shift negative wrapped phases back into the positive cycle")

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
