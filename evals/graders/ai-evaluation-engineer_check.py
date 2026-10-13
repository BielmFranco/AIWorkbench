import os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from candidate_fixture import Candidate
module=Candidate(Path(os.environ['AIWORKBENCH_OUTPUT_DIR'])/'solution.py')
expected={'ticket_id':'T17','category':'access'}
assert module.grade_ticket(expected.copy(),expected) is True, 'correct output'
assert module.grade_ticket({'category':'access','ticket_id':'T17'},expected) is True, 'alternative key order'
for output in ({'ticket_id':'T17','category':'billing'},{'category':'access'},{'ticket_id':17,'category':'access'},{'ticket_id':'T17','category':'access','extra':'x'},None,'text',[]):
    assert module.grade_ticket(output,expected) is False, f'false positive for {output!r}'

print('PASS: observed task outcomes')
