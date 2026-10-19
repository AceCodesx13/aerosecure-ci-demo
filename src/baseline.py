"""Baseline uses training outcomes only and evaluates on validation only."""
import json, statistics
from collections import defaultdict
from pathlib import Path
from validate_data import read
from schema import TARGET

root=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    train=read(root/'data/prepared/train/train.csv');validation=read(root/'data/prepared/validation/validation.csv');group=defaultdict(list)
    for r in train:group[r['part_category_id']].append(int(r[TARGET]))
    medians={k:statistics.median(v) for k,v in group.items()};fallback=statistics.median([int(r[TARGET]) for r in train])
    def score(predictions):
        errors=[int(r[TARGET])-p for r,p in zip(validation,predictions)]
        return dict(mae_days=round(statistics.mean(abs(e) for e in errors),3),underestimate_rate=round(statistics.mean(e>0 for e in errors),4))
    report=dict(evaluation_split='validation',row_count=len(validation),quoted_baseline=score([int(r['quoted_lead_time_days']) for r in validation]),historical_median_baseline=score([medians.get(r['part_category_id'],fallback) for r in validation]))
    out=root/'artifacts/reports';out.mkdir(parents=True,exist_ok=True);(out/'baseline_metrics.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
