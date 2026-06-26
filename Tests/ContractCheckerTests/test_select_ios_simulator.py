import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SELECTOR = ROOT / "scripts/select-ios-simulator.py"
PYTHON = ROOT / "scripts/run-python.sh"


class SimulatorSelectorTests(unittest.TestCase):
    def run_selector(self, devices):
        return subprocess.run(
            [str(PYTHON), str(SELECTOR)],
            input=json.dumps({"devices": devices}),
            text=True,
            capture_output=True,
        )

    def test_selects_highest_numeric_ios_runtime(self):
        result = self.run_selector(
            {
                "com.apple.CoreSimulator.SimRuntime.iOS-18-9": [
                    {"isAvailable": True, "name": "iPhone 16", "udid": "ios-18-9"}
                ],
                "com.apple.CoreSimulator.SimRuntime.iOS-18-10": [
                    {"isAvailable": True, "name": "iPhone 16", "udid": "ios-18-10"}
                ],
            }
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "ios-18-10")

    def test_ignores_runtimes_below_deployment_target(self):
        result = self.run_selector(
            {
                "com.apple.CoreSimulator.SimRuntime.iOS-9-3": [
                    {"isAvailable": True, "name": "iPhone 6s", "udid": "ios-9-3"}
                ]
            }
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("no available iPhone Simulator found", result.stderr)


if __name__ == "__main__":
    unittest.main()
