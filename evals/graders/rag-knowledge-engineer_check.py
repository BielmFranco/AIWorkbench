import os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from candidate_fixture import Candidate
module=Candidate(Path(os.environ['AIWORKBENCH_OUTPUT_DIR'])/'solution.py')
import copy
docs=[{'id':'a2','tenant':'A','current':True,'deleted':False},{'id':'a1','tenant':'A','current':False,'deleted':False},{'id':'b1','tenant':'B','current':True,'deleted':False},{'id':'gone','tenant':'A','current':True,'deleted':True}]
before=copy.deepcopy(docs)
for tenant, expected in (('A',{'a2'}),('B',{'b1'}),('unknown',set())):
    result=module.select_passages(docs,tenant)
    assert isinstance(result,(list,tuple,set)), 'return contract allows list, tuple or set only'
    assert set(result)==expected, 'ACL, revision, deletion and no-evidence behavior'
assert docs==before, 'do not mutate source lifecycle flags'

print('PASS: observed task outcomes')
