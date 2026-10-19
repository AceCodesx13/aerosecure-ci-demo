"""Convenience runner. The final test is a separate explicit step."""
import argparse,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--final-test',action='store_true');a=p.parse_args()
    steps=['evaluate.py'] if a.final_test else ['validate_data.py','baseline.py','train.py','predict.py','policy_demo.py']
    for step in steps:
        print('\nRunning '+step,flush=True);subprocess.run([sys.executable,str(ROOT/'src'/step)],cwd=ROOT,check=True)
    print('Done. See artifacts/reports/. Final test remains separate.' if not a.final_test else 'Final test report saved. Do not tune against it.')
