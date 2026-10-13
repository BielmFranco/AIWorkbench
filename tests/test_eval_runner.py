import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_evals import run_trial, trial_counts


class RunnerTests(unittest.TestCase):
    def test_live_trials_require_provider_completion(self):
        results = [{"provider_turn_completed": True}, {"provider_turn_completed": False}, {}, {"provider_turn_completed": 1}]
        self.assertEqual(trial_counts(results, "agent"), {"agent_adapter_executions":4,"live_trials":1})
        self.assertEqual(trial_counts(results, "simulation"), {"agent_adapter_executions":0,"live_trials":0})

    def test_paired_workspace_isolation_and_simulation_label(self):
        suite = json.loads((ROOT / "evals/cases/senior-software-engineer.json").read_text())
        case = next(c for c in suite["cases"] if c["mode"] == "outcome")
        adapter = {"kind":"simulation","command":[sys.executable,str(ROOT / "tests/fixture_adapter.py"),"--controls",str(ROOT / "evals/controls")]}
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            for condition in ("baseline", "candidate"):
                result = run_trial(ROOT, suite, case, condition, 1, destination, adapter, 30)
                self.assertEqual(result["verdict"]["status"], "passed", result)
                self.assertEqual(result["adapter_kind"], "simulation")
                run_dir = destination / case["id"] / condition / "1"
                self.assertTrue((run_dir / "result.json").exists())
                self.assertEqual((run_dir / "workspace/.agents/skills").exists(), condition == "candidate")
                self.assertFalse((run_dir / "workspace/evals/controls").exists())

    def test_case_path_cannot_escape_destination(self):
        suite = json.loads((ROOT / "evals/cases/senior-software-engineer.json").read_text())
        case = dict(next(c for c in suite["cases"] if c["mode"] == "outcome"))
        case["id"] = "../../escape"
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                run_trial(ROOT, suite, case, "candidate", 1, Path(temp), {"command":[],"kind":"simulation"}, 10)

    def test_malformed_observation_records_failure(self):
        suite = json.loads((ROOT / "evals/cases/senior-software-engineer.json").read_text())
        case = next(c for c in suite["cases"] if c["mode"] == "outcome")
        adapter = {"kind":"simulation","command":[sys.executable,"-c","import json,sys; from pathlib import Path; r=json.load(sys.stdin); Path(r['observation_path']).write_text('[]')"]}
        with tempfile.TemporaryDirectory() as temp:
            result = run_trial(ROOT, suite, case, "candidate", 1, Path(temp), adapter, 10)
            self.assertEqual(result["verdict"]["status"], "failed")
            self.assertIn("JSON object", result["verdict"]["reason"])


if __name__ == "__main__":
    unittest.main()
