"""Partition fictional raw records for a mentor's access-control exercise."""
import argparse,csv
from pathlib import Path
from schema import LABELS
from validate_data import read
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=root/'artifacts/access-tiers');a=p.parse_args();rows=read(root/'data/raw/orders.csv')
    for label in LABELS:
        subset=[r for r in rows if r['data_access_classification']==label];folder=a.output/label.lower().replace(' ','-');folder.mkdir(parents=True,exist_ok=True)
        with (folder/'orders.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(subset)
        print(label,':',len(subset),'rows at',folder/'orders.csv')
    print('Local partitions only. The mentor must enforce AWS permissions before uploading.')
