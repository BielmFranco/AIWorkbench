import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from eval_grading import contained, grade_case, grade_assertion


class GraderTests(unittest.TestCase):
    def test_all_known_controls_and_corrupt_outputs(self):
        for path in sorted((ROOT / "evals/cases").glob("*.json")):
            suite = json.loads(path.read_text())
            case = next(c for c in suite["cases"] if c["mode"] == "outcome")
            good = ROOT / "evals/controls" / suite["skill"] / "good"
            with self.subTest(skill=suite["skill"]):
                result = grade_case(case, good, ROOT)
                self.assertTrue(all(c["passed"] for c in result["checks"]), result)
                self.assertEqual(result["status"], "needs_review" if case["human_rubric"] else "passed")
                with tempfile.TemporaryDirectory() as temp:
                    bad = Path(temp)
                    (bad / "answer.json").write_text("{}", encoding="utf-8")
                    (bad / "solution.py").write_text("raise RuntimeError('corrupt control')\n", encoding="utf-8")
                    self.assertEqual(grade_case(case, bad, ROOT)["status"], "failed")

    def test_equal_json_numbers_allow_float_but_not_boolean(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            check = {"id":"numeric","kind":"json_value","artifact":"answer.json","pointer":"/n","expected":1}
            (output / "answer.json").write_text('{"n": 1.0}')
            self.assertTrue(grade_assertion(check, output, ROOT)["passed"])
            (output / "answer.json").write_text('{"n": true}')
            self.assertFalse(grade_assertion(check, output, ROOT)["passed"])

    def test_candidate_cannot_skip_checks_by_exiting_with_a_pass_marker(self):
        suite = json.loads((ROOT / "evals/cases/senior-software-engineer.json").read_text())
        case = next(c for c in suite["cases"] if c["mode"] == "outcome")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "solution.py").write_text("import sys\nprint('PASS: observed task outcomes')\nsys.exit(0)\n")
            self.assertEqual(grade_case(case, output, ROOT)["status"], "failed")

    def test_worker_preserves_return_type_contract(self):
        suite = json.loads((ROOT / "evals/cases/senior-software-engineer.json").read_text())
        case = next(c for c in suite["cases"] if c["mode"] == "outcome")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "solution.py").write_text("def process_events(events):\n    unique={}\n    for e in events: unique.setdefault(e['event_id'],e['receipt'])\n    return tuple(unique.values())\n")
            self.assertEqual(grade_case(case, output, ROOT)["status"], "failed")

    def test_worker_accepts_a_valid_unordered_iterable(self):
        suite = json.loads((ROOT / "evals/cases/rag-knowledge-engineer.json").read_text())
        case = next(c for c in suite["cases"] if c["mode"] == "outcome")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "solution.py").write_text("def select_passages(documents,tenant):\n    return {d['id'] for d in documents if d['tenant']==tenant and d['current'] and not d['deleted']}\n")
            self.assertEqual(grade_case(case, output, ROOT)["status"], "passed")

    def test_rag_grader_rejects_dictionary_as_passage_sequence(self):
        suite = json.loads((ROOT / "evals/cases/rag-knowledge-engineer.json").read_text())
        case = next(c for c in suite["cases"] if c["mode"] == "outcome")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "solution.py").write_text("def select_passages(documents,tenant):\n    return {d['id']:True for d in documents if d['tenant']==tenant and d['current'] and not d['deleted']}\n")
            self.assertEqual(grade_case(case, output, ROOT)["status"], "failed")

    def test_selection_needs_trace_not_self_report(self):
        case = {"mode":"routing","skill_under_test":"example","expected_skill":None}
        self.assertEqual(grade_case(case, ROOT, ROOT, {"selected_skills":[]})["status"], "ungraded")
        self.assertEqual(grade_case(case, ROOT, ROOT, {"capture_complete":True,"resource_reads":[]})["status"], "passed")
        case["expected_skill"] = "example"
        observation = {"resource_reads":[{"skill":"example","trace_ref":"trace:1","kind":"resource_read"}],"capture_complete":False}
        self.assertEqual(grade_case(case, ROOT, ROOT, observation)["status"], "passed")
        self.assertEqual(grade_case(case, ROOT, ROOT, [])["status"], "ungraded")

    def test_path_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            contained(ROOT, "../outside")


if __name__ == "__main__":
    unittest.main()
