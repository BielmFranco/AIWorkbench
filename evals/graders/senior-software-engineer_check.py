import os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from candidate_fixture import Candidate
module=Candidate(Path(os.environ['AIWORKBENCH_OUTPUT_DIR'])/'solution.py')
import copy
events=[{'event_id':'a','receipt':'r1'},{'event_id':'a','receipt':'wrong'},{'event_id':'b','receipt':'r2'}]
before=copy.deepcopy(events)
assert module.process_events(events)==['r1','r2'], 'duplicates must preserve first receipt and arrival order'
assert events==before, 'input was mutated'
assert module.process_events([])==[], 'empty input'
assert module.process_events([{'event_id':'z','receipt':'last'}])==['last'], 'single event'

print('PASS: observed task outcomes')
