"""Check the release without third-party dependencies."""
import csv, hashlib, json
from datetime import date
from pathlib import Path
from collections import Counter
from schema import *
from policy import shipment_decision

ROOT=Path(__file__).resolve().parents[1]
def read(path):
    with Path(path).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def validate(root=ROOT):
    d=root/'data';manifest=json.loads((d/'manifest.json').read_text());raw=read(d/'raw/orders.csv')
    assert manifest['total_orders']==len(raw)==20000,'Expected 20,000 orders'
    assert len(read(d/'reference/aircraft_models.csv'))==20
    associations=read(d/'reference/aircraft_parts.csv');assert len(associations)==400
    assert set(Counter(r['aircraft_model_id'] for r in associations).values())=={20}
    assert len({r['order_id'] for r in raw})==len(raw),'Duplicate order IDs'
    aircraft={r['aircraft_model_id'] for r in read(d/'reference/aircraft_models.csv')}
    part={r['part_category_id']:r for r in read(d/'reference/part_categories.csv')}
    suppliers={r['supplier_id']:r for r in read(d/'reference/suppliers.csv')}
    routes={(r['origin_region_id'],r['destination_region_id']):r for r in read(d/'reference/routes.csv')}
    eligibility={(r['supplier_id'],r['part_category_id']) for r in read(d/'reference/supplier_eligibility.csv')}
    policy={(r['shipment_restriction_classification'],r['destination_region_id']):r['destination_eligible']=='True' for r in read(d/'reference/shipment_policy.csv')}
    for r in raw:
        assert r['aircraft_model_id'] in aircraft and r['part_category_id'] in part
        assert (r['supplier_id'],r['part_category_id']) in eligibility
        assert r['condition'] in part[r['part_category_id']]['allowed_conditions'].split(';')
        assert r['origin_region_id']==suppliers[r['supplier_id']]['origin_region_id']
        route=routes[(r['origin_region_id'],r['destination_region_id'])]
        assert all(r[k]==route[k] for k in ['route_transit_days','route_customs_days'])
        assert r['data_access_classification'] in LABELS and r['shipment_restriction_classification'] in LABELS
        assert (date.fromisoformat(r['usable_receipt_date'])-date.fromisoformat(r['accepted_date'])).days==int(r[TARGET])>0
        assert int(r['order_month'])==date.fromisoformat(r['accepted_date']).month
        assert int(r['quantity_ordered'])>0 and all(float(r[k])>=0 for k in NUMERIC)
        if r['authorization_recorded_date']:assert r['authorization_recorded_date']<=r['accepted_date']
        assert shipment_decision(r['shipment_restriction_classification'],policy[(r['shipment_restriction_classification'],r['destination_region_id'])],r['authorization_status_at_acceptance'])[0]=='Allowed'
    raw_by_id={r['order_id']:r for r in raw};seen=set()
    for split in ['train','validation','test']:
        rows=read(d/'prepared'/split/(split+'.csv'));assert len(rows)==manifest['split_counts'][split]
        assert list(rows[0])==PREPARED_COLUMNS,'Prepared schema mismatch'
        for r in rows:
            assert r['order_id'] not in seen,'Split overlap';seen.add(r['order_id']);original=raw_by_id[r['order_id']]
            assert all(r[k]==original[k] for k in PREPARED_COLUMNS)
            if split=='train':assert r['accepted_date']<TRAIN_CUTOFF and original['usable_receipt_date']<TRAIN_CUTOFF
            elif split=='validation':assert TRAIN_CUTOFF<=r['accepted_date']<VALIDATION_CUTOFF and original['usable_receipt_date']<VALIDATION_CUTOFF
            else:assert r['accepted_date']>=VALIDATION_CUTOFF and original['usable_receipt_date']<OBSERVATION_END
        assert {r['aircraft_model_id'] for r in rows}==aircraft
        assert {r['part_category_id'] for r in rows}==set(part)
    excluded=read(d/'audit/excluded_at_boundary.csv');assert len(excluded)==manifest['excluded_count']
    assert seen.isdisjoint({r['order_id'] for r in excluded}) and len(seen)+len(excluded)==len(raw)
    for name,digest in manifest['sha256'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'Changed release file: '+name
    print('PASS: counts, schemas, references, conditions, policy, delivery dates, chronological splits, label maturity and file hashes')

if __name__=='__main__':validate()
