import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class WaveformExecutionContractTests(unittest.TestCase):
    maxDiff = None

    def run_mutation(self, name, mutate):
        with tempfile.TemporaryDirectory(prefix=f"sinewaveform-{name}-") as temporary:
            checkout = Path(temporary) / "repo"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git"))
            mutate(checkout)
            result = subprocess.run(
                ["/usr/bin/make", "test"],
                cwd=checkout,
                text=True,
                capture_output=True,
                timeout=120,
            )
        self.assertNotEqual(
            result.returncode,
            0,
            f"{name} bypassed the execution contract\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def replace_once(self, checkout, relative_path, old, new):
        path = checkout / relative_path
        source = path.read_text()
        self.assertEqual(source.count(old), 1, f"unexpected fixture for {relative_path}")
        path.write_text(source.replace(old, new, 1))

    def test_rejects_all_known_bypass_families(self):
        test_recipe = '''test:
\t"$$PYTHON" "$$ROOT/scripts/check-sinewaveform-source.py" --mode waveform
\t@if "$$SWIFTC" --available; then \\
\t\t"$$ROOT/scripts/run-waveform-math-tests.sh"; \\
\telse \\
\t\techo "swiftc not found; executable waveform math tests skipped"; \\
\tfi
\t@if "$$XCODEBUILD" --available; then \\
\t\t"$$ROOT/scripts/run-ios-render-tests.sh"; \\
\telse \\
\t\techo "xcodebuild not found; iOS rendering tests skipped"; \\
\tfi
'''
        runner_command = 'exec "$PYTHON" "$ROOT/scripts/verify-waveform-math-execution.py" --swiftc "$SWIFTC"'
        all_assertions_start = 'expectEqual(\n    "nan-fallback",'
        all_assertions_end = '\nguard assertionCount == 15 else {'

        def mutate_assertion_region(checkout, transform):
            path = checkout / "Tests/WaveformMathTests/main.swift"
            source = path.read_text()
            start = source.index(all_assertions_start)
            end = source.index(all_assertions_end)
            path.write_text(source[:start] + transform(source[start:end]) + source[end:])

        mutations = {
            "runner_if_false": lambda checkout: self.replace_once(
                checkout,
                "scripts/run-waveform-math-tests.sh",
                runner_command,
                f"if false; then\n    {runner_command}\nfi",
            ),
            "make_if_false": lambda checkout: self.replace_once(
                checkout,
                "Makefile",
                'if "$$SWIFTC" --available; then \\\n',
                "if false; then \\\n",
            ),
            "make_comment": lambda checkout: self.replace_once(
                checkout,
                "Makefile",
                test_recipe,
                '''test:
\t"$$PYTHON" "$$ROOT/scripts/check-sinewaveform-source.py" --mode waveform
\t@# "$$ROOT/scripts/run-waveform-math-tests.sh"
''',
            ),
            "make_string": lambda checkout: self.replace_once(
                checkout,
                "Makefile",
                test_recipe,
                '''test:
\t"$$PYTHON" "$$ROOT/scripts/check-sinewaveform-source.py" --mode waveform
\t@printf '%s\n' '"$$ROOT/scripts/run-waveform-math-tests.sh"'
''',
            ),
            "render_runner_removed": lambda checkout: self.replace_once(
                checkout,
                "Makefile",
                '\t\t"$$ROOT/scripts/run-ios-render-tests.sh"; \\\n',
                '\t\t:; \\\n',
            ),
            "programmatic_opacity_only_in_comment": lambda checkout: self.replace_once(
                checkout,
                "SineWaveform/SineWaveForm.swift",
                "        isOpaque = false\n    }\n\n    public required init?(coder: NSCoder)",
                "        // isOpaque = false\n    }\n\n    public required init?(coder: NSCoder)",
            ),
            "decoded_opacity_only_in_comment": lambda checkout: self.replace_once(
                checkout,
                "SineWaveform/SineWaveForm.swift",
                "    public required init?(coder: NSCoder) {\n        super.init(coder: coder)\n        isOpaque = false\n",
                "    public required init?(coder: NSCoder) {\n        super.init(coder: coder)\n        // isOpaque = false\n",
            ),
            "swift_if_false": lambda checkout: mutate_assertion_region(
                checkout, lambda region: f"if false {{\n{region}\n}}\n"
            ),
            "swift_block_comment": lambda checkout: mutate_assertion_region(
                checkout, lambda region: f"/*\n{region}\n*/\n"
            ),
            "swift_string": lambda checkout: mutate_assertion_region(
                checkout, lambda region: f'let inertAssertions = """\n{region}\n"""\n_ = inertAssertions\n'
            ),
            "swift_unreachable_comparison": lambda checkout: self.replace_once(
                checkout,
                "Tests/WaveformMathTests/main.swift",
                ") {\n    assertionCount += 1\n    if !actual.isFinite",
                ") {\n    assertionCount += 1\n    return ()\n    if !actual.isFinite",
            ),
            "swift_erased_failure": lambda checkout: (
                self.replace_once(
                    checkout,
                    "Tests/WaveformMathTests/main.swift",
                    "    forceFailure ? 0.50 : 0.25,",
                    "    0.50,",
                ),
                self.replace_once(
                    checkout,
                    "Tests/WaveformMathTests/main.swift",
                    "guard failureCount == 0 else {",
                    "failureCount = 0\nguard failureCount == 0 else {",
                ),
            ),
            "runner_forged_success": lambda checkout: self.replace_once(
                checkout,
                "scripts/run-waveform-math-tests.sh",
                runner_command,
                f'if [ "${{SINEWAVEFORM_CONTRACT_MUTATION_CHILD:-}}" = 1 ]; then\n    {runner_command}\nelse\n    echo "WaveformMath execution verified: 15 assertions and negative control"\nfi',
            ),
        }

        for name, mutate in mutations.items():
            with self.subTest(name=name):
                self.run_mutation(name, mutate)

    def test_rejects_additional_adversarial_mutations(self):
        runner_command = 'exec "$PYTHON" "$ROOT/scripts/verify-waveform-math-execution.py" --swiftc "$SWIFTC"'
        mutations = {
            "runner_exit_before_execution": lambda checkout: self.replace_once(
                checkout,
                "scripts/run-waveform-math-tests.sh",
                runner_command,
                f"exit 0\n{runner_command}",
            ),
            "runner_commented_execution": lambda checkout: self.replace_once(
                checkout,
                "scripts/run-waveform-math-tests.sh",
                runner_command,
                f"# {runner_command}",
            ),
            "runner_echoed_execution": lambda checkout: self.replace_once(
                checkout,
                "scripts/run-waveform-math-tests.sh",
                runner_command,
                f"printf '%s\\n' '{runner_command}'",
            ),
            "runner_uninvoked_function": lambda checkout: self.replace_once(
                checkout,
                "scripts/run-waveform-math-tests.sh",
                runner_command,
                f"run_tests() {{\n    {runner_command}\n}}",
            ),
            "make_exit_before_execution": lambda checkout: self.replace_once(
                checkout,
                "Makefile",
                '\t@if "$$SWIFTC" --available; then \\\n',
                '\t@exit 0; # if "$$SWIFTC" --available; then \\\n',
            ),
            "swift_comparison_always_false": lambda checkout: self.replace_once(
                checkout,
                "Tests/WaveformMathTests/main.swift",
                "if !actual.isFinite || abs(actual - expected) > accuracy {",
                "if false && (!actual.isFinite || abs(actual - expected) > accuracy) {",
            ),
            "swift_failure_guard_disabled": lambda checkout: self.replace_once(
                checkout,
                "Tests/WaveformMathTests/main.swift",
                "guard failureCount == 0 else {",
                "guard true || failureCount == 0 else {",
            ),
            "swift_static_completion": lambda checkout: self.replace_once(
                checkout,
                "Tests/WaveformMathTests/main.swift",
                'print("COMPLETE \\(nonce) \\(assertionCount)")',
                'print("COMPLETE \\(nonce) 15")',
            ),
            "verifier_skips_positive_process": lambda checkout: self.replace_once(
                checkout,
                "scripts/verify-waveform-math-execution.py",
                'passing = run(binary, pass_nonce, "normal")',
                'passing = subprocess.CompletedProcess([], 0, expected_pass_output(pass_nonce), "")',
            ),
            "verifier_skips_negative_process": lambda checkout: self.replace_once(
                checkout,
                "scripts/verify-waveform-math-execution.py",
                'failing = run(binary, failure_nonce, "force-failure")',
                'failing = subprocess.CompletedProcess([], 1, expected_failure_stdout, expected_failure)',
            ),
            "verifier_fixed_nonce": lambda checkout: self.replace_once(
                checkout,
                "scripts/verify-waveform-math-execution.py",
                "pass_nonce = os.urandom(32).hex()",
                'pass_nonce = "0" * 64',
            ),
            "production_math_always_zero": lambda checkout: self.replace_once(
                checkout,
                "SineWaveform/WaveformMath.swift",
                "return normalizedValue(value, minimum: 0.0, maximum: 1.0, fallback: 0.0)",
                "return 0.0",
            ),
        }

        for name, mutate in mutations.items():
            with self.subTest(name=name):
                self.run_mutation(name, mutate)

    def test_checker_does_not_echo_repository_content(self):
        marker = "SINEWAVEFORM_SECRET_MARKER_DO_NOT_PRINT"
        with tempfile.TemporaryDirectory(prefix="sinewaveform-diagnostic-redaction-") as temporary:
            checkout = Path(temporary) / "repo"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git"))
            (checkout / "docs/device-preview.svg").write_text(f"<{marker}>")
            result = subprocess.run(
                [
                    str(checkout / "scripts/run-python.sh"),
                    str(checkout / "scripts/check-sinewaveform-source.py"),
                    "--mode",
                    "package",
                ],
                cwd=checkout,
                text=True,
                capture_output=True,
                timeout=120,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(marker, result.stderr)
        self.assertRegex(result.stderr, r"package checks failed: \d+ validation error\(s\)")
        self.assertNotIn("must be valid XML", result.stderr)


if __name__ == "__main__":
    unittest.main()
