import os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from candidate_fixture import Candidate
module=Candidate(Path(os.environ['AIWORKBENCH_OUTPUT_DIR'])/'solution.py')
class Provider:
    def __init__(self, mode): self.mode=mode; self.calls=[]; self.effects=0
    def refund(self,key):
        self.calls.append(('refund',key))
        if self.mode=='denied': return 'denied'
        if self.mode=='pending': return 'pending'
        self.effects+=1
        raise TimeoutError('response lost')
    def lookup(self,key):
        self.calls.append(('lookup',key))
        return 'issued' if self.effects else 'pending'
p=Provider('lost')
assert module.resolve(p,'k1',3)=='issued', 'must resolve effect after lost response'
assert p.effects==1 and p.calls==[('refund','k1'),('lookup','k1')], 'lookup original key before another mutation'
p=Provider('pending')
assert module.resolve(p,'k2',2)=='unresolved' and len(p.calls)<=2, 'bounded unresolved recovery'
p=Provider('denied')
assert module.resolve(p,'k3',3)=='denied' and p.effects==0, 'denied requests must not mutate'
try: module.resolve(p,'k4',0)
except ValueError: pass
else: raise AssertionError('invalid budget must be rejected')

print('PASS: observed task outcomes')
