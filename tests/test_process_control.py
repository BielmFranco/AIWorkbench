from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from process_control import run_bounded


class ProcessTests(unittest.TestCase):
    def test_timeout_stops_the_execution(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            run_bounded([sys.executable, "-c", "import time; time.sleep(30)"], timeout=0.2)

    def test_timeout_cleans_descendant_after_parent_exit(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp) / "descendant-survived"
            child_code = "import time; from pathlib import Path; time.sleep(1); Path(" + repr(str(marker)) + ").write_text('survived')"
            parent_code = "import subprocess,sys; subprocess.Popen([sys.executable,'-c'," + repr(child_code) + "]); sys.exit(0)"
            with self.assertRaises(subprocess.TimeoutExpired):
                run_bounded([sys.executable, "-c", parent_code], timeout=0.2)
            time.sleep(1.1)
            self.assertFalse(marker.exists(), "descendant survived process-tree cleanup")


if __name__ == "__main__":
    unittest.main()
