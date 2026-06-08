#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-sinewaveform-baseline.md"


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
    if "let waveCount = max(1, numOfWaves)" not in source:
        errors.append("drawRect must clamp wave count to at least 1")
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
