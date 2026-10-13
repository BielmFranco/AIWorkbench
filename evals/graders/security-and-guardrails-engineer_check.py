import os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from candidate_fixture import Candidate
module=Candidate(Path(os.environ['AIWORKBENCH_OUTPUT_DIR'])/'solution.py')
assert module.can_refund({'account_id':'A','authenticated':True},{'owner':'A'}) is True, 'legitimate owner'
assert module.can_refund({'account_id':'A','authenticated':True},{'owner':'B'}) is False, 'cross-account denied'
assert module.can_refund({'account_id':'A','authenticated':False},{'owner':'A'}) is False, 'unauthenticated denied'
assert module.can_refund({'account_id':'A','authenticated':1},{'owner':'A'}) is False, 'truthy value must not replace authenticated boolean'
for principal,charge in (({},{}),(None,{'owner':'A'}),({'authenticated':True},{'owner':None})):
    assert module.can_refund(principal,charge) is False, 'missing identity denied'

print('PASS: observed task outcomes')
