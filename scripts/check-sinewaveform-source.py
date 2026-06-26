#!/usr/bin/env python3
import argparse
import _hashlib
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
MAKE_AUTHORITY_PLAN = DOCS_PLANS / "2026-06-21-make-authority-isolation.md"
INSTALLATION_DOCS_PLAN = DOCS_PLANS / "2026-06-25-installation-naming.md"
RENDER_TEST = ROOT / "Tests" / "SineWaveformRenderTests" / "SineWaveformRenderTests.swift"
RENDER_TEST_RUNNER = ROOT / "scripts" / "run-ios-render-tests.sh"
SHARED_SCHEME = ROOT / "SineWaveform.xcodeproj" / "xcshareddata" / "xcschemes" / "SineWaveform.xcscheme"
WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"
EXECUTION_CONTRACT_HASHES = {
    "Makefile": "b66569b22fc20a854b9bdb041dfb19e8ff16db54ecd200462883f69f882bce79",
    "Tests/WaveformMathTests/main.swift": "735ef34cc9affe9efe44e015a722d6632e2ea85c250fb7db7c656b6021e59b24",
    "scripts/run-waveform-math-tests.sh": "156169416ec43dae2730fbf22dfac7ddc87fce9c1da05faa4863615b301b153b",
    "scripts/verify-waveform-math-execution.py": "eb5042f68e29d1b5840083da440b3ebf6b87ece2e7ac321b7ca6226fdb789cbb",
}

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
        "SineWaveform.xcodeproj/xcshareddata/xcschemes/SineWaveform.xcscheme",
        "Tests/SineWaveformRenderTests/SineWaveformRenderTests.swift",
        "Tests/WaveformMathTests/main.swift",
        "scripts/select-ios-simulator.py",
        "scripts/run-ios-render-tests.sh",
        "scripts/run-waveform-math-tests.sh",
        "scripts/run-python.sh",
        "scripts/run-ruby.sh",
        "scripts/run-swiftc.sh",
        "scripts/run-xcodebuild.sh",
        "scripts/test-makefile-root.sh",
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
    if not MAKE_AUTHORITY_PLAN.exists():
        errors.append("docs/plans/2026-06-21-make-authority-isolation.md is missing")
    if not INSTALLATION_DOCS_PLAN.exists():
        errors.append("docs/plans/2026-06-25-installation-naming.md is missing")

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

    for fragment in (
        "## Installation",
        "pod 'SineWaveform', :git => 'https://github.com/garethpaul/sinewaveform.git', :branch => 'master'",
        "import SineWaveform",
        "let waveformView = SiriWaveformView(frame: .zero)",
        "waveformView.updateWithLevel(0.5)",
        "The CocoaPods and Swift module name is `SineWaveform`",
        "The public view type is `SiriWaveformView`",
        "docs/plans/2026-06-25-installation-naming.md",
    ):
        if fragment not in readme:
            errors.append(f"README installation contract is missing: {fragment}")
    for incorrect_fragment in (
        "pod 'sinewaveform'",
        "import sinewaveform",
        ":tag => '0.0.6'",
    ):
        if incorrect_fragment in readme:
            errors.append(f"README must not use incorrect package naming: {incorrect_fragment}")

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
    root_declaration = "override ROOT := $(shell path='$(subst ','\"'\"',$(value MAKEFILE_LIST))'; path=$$(printf '%s' \"$$path\" | /usr/bin/sed 's/^ //'); [ -f \"$$path\" ] || exit 1; directory=$$(/usr/bin/dirname -- \"$$path\"); CDPATH= cd -- \"$$directory\" && /bin/pwd -P)"
    if makefile.count(root_declaration) != 1:
        errors.append("Makefile must contain exactly one protected repository-root declaration")

    for fragment in (
        ".DEFAULT_GOAL := check",
        ".PHONY: __repository-make-authority build check contract-test lint root-test test verify",
        ".SECONDEXPANSION:",
        "override SHELL := /bin/sh",
        "override .SHELLFLAGS := -c",
        "override PYTHONDONTWRITEBYTECODE := 1",
        "$(error MAKEFLAGS must not be overridden for repository verification)",
        "$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)",
        "$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)",
        "$(error MAKEFILE_LIST must not be overridden)",
        "$(error repository Makefile must be loaded alone)",
        root_declaration,
        "$(error repository Makefile path could not be resolved)",
        "override PYTHON := $(ROOT)/scripts/run-python.sh",
        "override RUBY := $(ROOT)/scripts/run-ruby.sh",
        "override SWIFTC := $(ROOT)/scripts/run-swiftc.sh",
        "override XCODEBUILD := $(ROOT)/scripts/run-xcodebuild.sh",
        "override TMPDIR := /tmp",
        "override XCODEBUILD_DERIVED_DATA_PATH := $(TMPDIR)/sinewaveform-derived-data",
        "build: lint",
        "root-test:",
        '"$$RUBY" -c "$$ROOT/SineWaveform.podspec"',
        '"$$PYTHON" "$$ROOT/scripts/check-sinewaveform-source.py" --mode package',
        'if "$$SWIFTC" --available; then',
        '"$$ROOT/scripts/run-waveform-math-tests.sh"',
        'if "$$XCODEBUILD" --available; then',
        '"$$XCODEBUILD" -project "$$ROOT/SineWaveform.xcodeproj"',
        '-derivedDataPath "$$XCODEBUILD_DERIVED_DATA_PATH"',
        '"$$PYTHON" -m unittest discover',
        '"$$ROOT/scripts/test-makefile-root.sh"',
        "verify: root-test lint contract-test test build",
        "check: verify",
        "-scheme SineWaveform",
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
    if str(MAKE_AUTHORITY_PLAN.relative_to(ROOT)) not in read_text("README.md"):
        errors.append("README must index Make authority isolation evidence")

    trusted_launchers = {
        "scripts/run-python.sh": (
            'exec /usr/bin/python3 -I -B "$@"',
            "runpy.run_path",
        ),
        "scripts/run-ruby.sh": ('exec /usr/bin/ruby "$@"',),
        "scripts/run-swiftc.sh": (
            "/usr/bin/swiftc /usr/local/swift/usr/bin/swiftc",
            'if [ "${1:-}" = --available ]',
            'exec "$compiler" "$@"',
        ),
        "scripts/run-xcodebuild.sh": (
            'if [ "${1:-}" = --available ]',
            'exec /usr/bin/xcodebuild "$@"',
        ),
    }
    for relative_path, fragments in trusted_launchers.items():
        launcher = read_text(relative_path)
        for fragment in fragments:
            if fragment not in launcher:
                errors.append(
                    f"{relative_path} must preserve trusted launcher fragment {fragment!r}"
                )

    runner = read_text("scripts/run-waveform-math-tests.sh")
    for fragment in (
        'PYTHON="$ROOT/scripts/run-python.sh"',
        'SWIFTC="$ROOT/scripts/run-swiftc.sh"',
    ):
        if fragment not in runner:
            errors.append(f"scripts/run-waveform-math-tests.sh must preserve {fragment}")

    contract_tests = read_text("Tests/ContractCheckerTests/test_waveform_execution_contract.py")
    if '["/usr/bin/make", "test"]' not in contract_tests:
        errors.append("contract mutation tests must invoke the trusted absolute GNU Make path")

    root_test = read_text("scripts/test-makefile-root.sh")
    for evidence in (
        "147 executed target/authority cases",
        "2 MAKEFILE_LIST rejections",
        "3 contained startup-boundary cases",
        "10 mode-flag rejections",
        "SINEWAVEFORM_DOLLAR_MARKER",
    ):
        if evidence not in root_test:
            errors.append(f"scripts/test-makefile-root.sh must preserve {evidence!r}")

    if MAKE_AUTHORITY_PLAN.exists():
        authority_plan = MAKE_AUTHORITY_PLAN.read_text(encoding="utf-8")
        for evidence in (
            "Status: Completed",
            "`make root-test` passed 133 target/authority cases",
            "visible additional files are rejected before recipes",
            "Repository and external-directory `make check` passed",
        ):
            if evidence not in authority_plan:
                errors.append(f"{MAKE_AUTHORITY_PLAN.relative_to(ROOT)} must record {evidence!r}")

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
    executable_source = re.sub(r"//[^\n]*", "", source)
    math_source = read_text("SineWaveform/WaveformMath.swift")
    render_test = RENDER_TEST.read_text(encoding="utf-8")
    render_test_runner = RENDER_TEST_RUNNER.read_text(encoding="utf-8")
    project = read_text("SineWaveform.xcodeproj/project.pbxproj")
    scheme = SHARED_SCHEME.read_text(encoding="utf-8")
    makefile = read_text("Makefile")
    test_source = read_text("Tests/WaveformMathTests/main.swift")
    test_runner = read_text("scripts/run-waveform-math-tests.sh")
    for relative_path, expected_hash in EXECUTION_CONTRACT_HASHES.items():
        actual_hash = _hashlib.openssl_sha256((ROOT / relative_path).read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"waveform execution contract file changed unexpectedly: {relative_path}")
    for fragment in (
        "testDefaultViewUsesNonopaqueCompositing",
        "testDecodedViewUsesNonopaqueCompositing",
        "testNilBackgroundLeavesRenderedPixelTransparent",
        "testTranslucentBackgroundIsCompositedOnce",
        "original.isOpaque = true",
        "format.opaque = false",
        "view.layer.render(in: context.cgContext)",
        "return pixel[3]",
    ):
        if fragment not in render_test:
            errors.append(f"iOS rendering test coverage is missing: {fragment}")
    for fragment in (
        "/usr/bin/xcrun simctl list devices available -j",
        '"$ROOT/scripts/select-ios-simulator.py"',
        'exec "$XCODEBUILD"',
        "CODE_SIGNING_ALLOWED=NO",
        "test",
    ):
        if fragment not in render_test_runner:
            errors.append(f"iOS rendering test runner is missing: {fragment}")
    for fragment in (
        "SineWaveformRenderTests.xctest",
        "com.apple.product-type.bundle.unit-test",
        "SineWaveformRenderTests.swift in Sources",
        "PBXTargetDependency",
    ):
        if fragment not in project:
            errors.append(f"Xcode render-test target is missing: {fragment}")
    for fragment in (
        'BlueprintName = "SineWaveformRenderTests"',
        "<TestableReference",
        'skipped = "NO"',
    ):
        if fragment not in scheme:
            errors.append(f"shared render-test scheme is missing: {fragment}")
    if makefile.count('"$$ROOT/scripts/run-ios-render-tests.sh"') != 1:
        errors.append("make test must execute the iOS rendering test runner exactly once")
    for initializer, pattern in (
        (
            "programmatic",
            r"public override init\(frame: CGRect\) \{\s*"
            r"super\.init\(frame: frame\)\s*"
            r"isOpaque = false\s*\}",
        ),
        (
            "decoded",
            r"public required init\?\(coder: NSCoder\) \{\s*"
            r"super\.init\(coder: coder\)\s*"
            r"isOpaque = false\s*\}",
        ),
    ):
        if re.search(pattern, source) is None:
            errors.append(f"{initializer} waveform views must initialize nonopaque compositing")
    background_fill = (
        r"if let backgroundColor = backgroundColor \{\s*"
        r"context\.setFillColor\(backgroundColor\.cgColor\)\s*"
        r"context\.fill\(rect\)\s*\}"
    )
    if re.search(background_fill, executable_source) is None:
        errors.append("explicit waveform backgrounds must be restored after the context clear")
    if "backgroundColor?.set()" in executable_source:
        errors.append("a nil waveform background must not select an implicit fill color")
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
        "return normalizedValue(value, minimum: 0.0, maximum: 1.0, fallback: 0.0)",
        "return max(step, width / CGFloat(maximumSampleIntervalCount))",
        "return index == maximumSampleIntervalCount ? width : min(accumulatedX, width)",
    ):
        if fragment not in math_source:
            errors.append(f"shared executable waveform math is missing: {fragment}")
    for fragment in (
        "if !actual.isFinite || abs(actual - expected) > accuracy",
        "assertionCount += 1",
        "guard assertionCount == 15",
        "guard failureCount == 0",
        'print("ASSERT \\(nonce) \\(identifier) PASS")',
        'print("COMPLETE \\(nonce) \\(assertionCount)")',
        "WaveformMath.normalizedValue(.nan",
        "WaveformMath.normalizedPhase(-0.5",
        "WaveformMath.sampleStep(width: 8190.0",
        "WaveformMath.sampleX(index: 4095",
    ):
        if fragment not in test_source:
            errors.append(f"executable waveform behavior coverage is missing: {fragment}")
    for fragment in (
        'PYTHON="$ROOT/scripts/run-python.sh"',
        'SWIFTC="$ROOT/scripts/run-swiftc.sh"',
        'exec "$PYTHON" "$ROOT/scripts/verify-waveform-math-execution.py" --swiftc "$SWIFTC"',
    ):
        if fragment not in test_runner:
            errors.append(f"waveform behavior test runner is missing: {fragment}")
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
        print(f"{args.mode} checks failed: {len(errors)} validation error(s)", file=sys.stderr)
        for index in range(1, len(errors) + 1):
            print(f"validation error {index}", file=sys.stderr)
        return 1
    print(f"{args.mode} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
