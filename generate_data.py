"""Generate versioned fictional catalogs and 20,000 completed orders, using stdlib only."""
import argparse, csv, hashlib, json, math, random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from schema import *
from policy import shipment_decision

AIRCRAFT = [
 ('Airbus','A220-100','Small single-aisle jet'),('Airbus','A220-300','Small single-aisle jet'),
 ('Airbus','A320neo','Single-aisle jet'),('Airbus','A321neo','Single-aisle jet'),
 ('Airbus','A330-900','Widebody jet'),('Airbus','A350-900','Widebody jet'),
 ('Boeing','737-800','Single-aisle jet'),('Boeing','737-8','Single-aisle jet'),
 ('Boeing','777-300ER','Widebody jet'),('Boeing','787-8','Widebody jet'),('Boeing','787-9','Widebody jet'),
 ('Embraer','E170','Regional jet'),('Embraer','E175','Regional jet'),('Embraer','E190','Regional jet'),
 ('Embraer','E195-E2','Regional jet'),('ATR','ATR 42-600','Regional turboprop'),('ATR','ATR 72-600','Regional turboprop'),
 ('De Havilland Canada','Dash 8-100','Regional turboprop'),('De Havilland Canada','Dash 8-300','Regional turboprop'),('De Havilland Canada','Dash 8-400','Regional turboprop')]
PARTS = [
 ('Engine oil filter','Consumable',5),('Hydraulic filter','Consumable',6),('Fuel filter','Consumable',6),
 ('Main wheel tire','Consumable',9),('Nose wheel tire','Consumable',8),('Brake friction element','Consumable',12),
 ('Hydraulic seal kit','Consumable',5),('O-ring kit','Consumable',4),('Wheel bearing','Repairable',12),
 ('Hydraulic pressure sensor','Repairable',16),('Temperature sensor','Repairable',14),('Fuel quantity sensor','Repairable',18),
 ('Hydraulic control valve','Repairable',22),('Fuel pump','Repairable',24),('Hydraulic pump','Repairable',26),
 ('Navigation light assembly','Repairable',12),('Engine assembly','Major',85),('Landing-gear assembly','Major',70),
 ('Environmental control unit','Major',55),('Flight-control actuator assembly','Major',45)]
SUPPLIERS = [
 ('SUP-A','Aster Consumables','REG-A','Consumable',2,0.7),('SUP-B','Beacon Wheels and Brakes','REG-B','Consumable',5,1.1),
 ('SUP-C','Cedar Component Repair','REG-A','Repairable',7,1.0),('SUP-D','Delta Assembly Services','REG-C','Major',10,1.3),
 ('SUP-E','Evergreen Engine Services','REG-B','Major',8,1.1),('SUP-F','Falcon Consumables','REG-C','Consumable',4,0.9),
 ('SUP-G','Granite Components','REG-B','Repairable',5,0.9),('SUP-H','Harbor Assembly Repair','REG-A','Major',7,1.0),
 ('SUP-I','Indigo Components','REG-C','Repairable',9,1.2)]

def write_csv(path, rows, columns=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns or list(rows[0]));w.writeheader();w.writerows(rows)

def generate(root, seed=SEED):
    rng=random.Random(seed);data=root/'data';ref=data/'reference'
    aircraft=[dict(aircraft_model_id=f'AC-{i+1:02}',manufacturer=m,model=n,aircraft_category=c,compatibility_scope='Illustrative classroom associations only') for i,(m,n,c) in enumerate(AIRCRAFT)]
    parts=[dict(part_category_id=f'PC-{i+1:02}',part_category=n,part_group=g,simulated_base_days=b,allowed_conditions='New' if g=='Consumable' else 'New;Repaired;Overhauled') for i,(n,g,b) in enumerate(PARTS)]
    associations=[dict(aircraft_part_id=f'{a["aircraft_model_id"]}-{pc["part_category_id"]}',aircraft_model_id=a['aircraft_model_id'],part_category_id=pc['part_category_id'],part_number='SIM-'+a['aircraft_model_id']+'-'+pc['part_category_id'],association_status='Illustrative, not verified aircraft compatibility') for a in aircraft for pc in parts]
    suppliers=[dict(supplier_id=i,name=n,origin_region_id=r,specialty_group=g,simulated_handling_days=h,simulated_replenishment_factor=f) for i,n,r,g,h,f in SUPPLIERS]
    regions=[dict(region_id=f'REG-{c}',name=f'Fictional Region {c}',real_geographic_mapping='None') for c in 'ABC']
    routes=[dict(origin_region_id=o['region_id'],destination_region_id=d['region_id'],route_transit_days=2 if o==d else 6+(ord(o['region_id'][-1])+ord(d['region_id'][-1]))%3,route_customs_days=0 if o==d else 3) for o in regions for d in regions]
    policy=[dict(shipment_restriction_classification=l,destination_region_id=r['region_id'],destination_eligible=not(l=='Highly Restricted' and r['region_id']=='REG-C'),requirement='None' if l==LABELS[0] else 'Valid authorization' if l==LABELS[1] else 'Human review and approval') for l in LABELS for r in regions]
    eligibility=[dict(supplier_id=s['supplier_id'],part_category_id=pc['part_category_id'],allowed_conditions=pc['allowed_conditions']) for s in suppliers for pc in parts if s['specialty_group']==pc['part_group']]
    for name,rows in [('aircraft_models',aircraft),('part_categories',parts),('aircraft_parts',associations),('suppliers',suppliers),('regions',regions),('routes',routes),('shipment_policy',policy),('supplier_eligibility',eligibility)]:write_csv(ref/(name+'.csv'),rows)
    orders=[]
    for round_index in range(50):
        for a in aircraft:
            for pc in parts:
                sup=rng.choice([s for s in suppliers if s['specialty_group']==pc['part_group']])
                classification=rng.choice(LABELS);access=rng.choice(LABELS)
                dest=rng.choice(['REG-A','REG-B'] if classification==LABELS[2] else ['REG-A','REG-B','REG-C'])
                route=next(r for r in routes if r['origin_region_id']==sup['origin_region_id'] and r['destination_region_id']==dest)
                accepted=date(2024,1,1)+timedelta(days=round_index*12+rng.randrange(9))
                condition=rng.choice(pc['allowed_conditions'].split(';'));qty=rng.randint(1,20) if pc['part_group']=='Consumable' else rng.randint(1,4)
                stock=rng.randint(0,30) if pc['part_group']=='Consumable' else rng.randint(0,3)
                backlog=rng.randint(0,25);shortfall=max(0,qty-stock);season=5 if accepted.month in [11,12] else 0
                replenish=(pc['simulated_base_days']*sup['simulated_replenishment_factor']+shortfall*1.8) if shortfall else 0
                repair=0 if condition=='New' else 10 if condition=='Repaired' else 17
                expected=sup['simulated_handling_days']+route['route_transit_days']+route['route_customs_days']+replenish+0.65*backlog+repair+season
                quoted=max(1,round(expected+rng.gauss(-3,5)))
                # Unobservable shocks never appear in the feature file.
                shock=rng.randint(8,25) if rng.random()<0.07 else 0
                actual=max(1,round(expected+rng.gauss(0,3 if pc['part_group']=='Consumable' else 6)+shock))
                auth='Not required' if classification==LABELS[0] else 'Valid' if classification==LABELS[1] else 'Approved after review'
                row=dict(order_id=f'ORD-{len(orders)+1:06}',accepted_date=accepted.isoformat(),aircraft_model_id=a['aircraft_model_id'],part_category_id=pc['part_category_id'],supplier_id=sup['supplier_id'],condition=condition,origin_region_id=sup['origin_region_id'],destination_region_id=dest,quantity_ordered=qty,stock_at_acceptance=stock,supplier_backlog_days=backlog,quoted_lead_time_days=quoted,route_transit_days=route['route_transit_days'],route_customs_days=route['route_customs_days'],order_month=accepted.month,actual_delivery_days=actual,usable_receipt_date=(accepted+timedelta(days=actual)).isoformat(),order_status='Completed',data_access_classification=access,shipment_restriction_classification=classification,authorization_status_at_acceptance=auth,authorization_recorded_date='' if auth=='Not required' else (accepted-timedelta(days=1)).isoformat(),source_type='Synthetic')
                orders.append(row)
    orders.sort(key=lambda r:(r['accepted_date'],r['order_id']))
    write_csv(data/'raw/orders.csv',orders)
    splits={'train':[],'validation':[],'test':[]};excluded=[]
    for r in orders:
        split='train' if r['accepted_date']<TRAIN_CUTOFF else 'validation' if r['accepted_date']<VALIDATION_CUTOFF else 'test'
        maturity=TRAIN_CUTOFF if split=='train' else VALIDATION_CUTOFF if split=='validation' else OBSERVATION_END
        if r['usable_receipt_date']>=maturity:
            excluded.append(dict(order_id=r['order_id'],candidate_split=split,reason='Outcome not yet known at split boundary'));continue
        splits[split].append({c:r[c] for c in PREPARED_COLUMNS})
    for split,rows in splits.items():write_csv(data/'prepared'/split/(split+'.csv'),rows,PREPARED_COLUMNS)
    write_csv(data/'audit/excluded_at_boundary.csv',excluded)
    # Tiny AWS smoke subset retains exactly the same schema and feature definitions.
    for split,rows in splits.items():write_csv(data/'smoke'/split/(split+'.csv'),rows[:min(800 if split=='train' else 200,len(rows))],PREPARED_COLUMNS)
    sample=[]
    for r in splits['test'][:5]:sample.append({c:r[c] for c in ['order_id']+FEATURES})
    write_csv(data/'examples/new_orders.csv',sample)
    scenarios=[
      ('SC-01','Unrestricted','REG-A','Not required','Allowed'),('SC-02','Restricted','REG-B','Valid','Allowed'),
      ('SC-03','Restricted','REG-A','Missing','Review required'),('SC-04','Restricted','REG-A','Expired','Review required'),
      ('SC-05','Highly Restricted','REG-B','Approved after review','Allowed'),('SC-06','Highly Restricted','REG-C','Approved after review','Blocked'),
      ('SC-07','Highly Restricted','REG-A','Valid','Review required'),('SC-08','Unknown','REG-A','Missing','Review required'),
      ('SC-09','Unrestricted','UNKNOWN','Not required','Review required')]
    write_csv(data/'examples/policy_scenarios.csv',[dict(scenario_id=i,shipment_restriction_classification=l,destination_region_id=d,authorization_status=a,expected_decision=e) for i,l,d,a,e in scenarios])
    # Scenarios only: hour-based maintenance arithmetic is fictional and separate from model training.
    write_csv(data/'examples/maintenance_scenarios.csv',[
      dict(scenario_id='M-01',aircraft_part_id='AC-01-PC-02',scenario_date='2026-10-12',replacement_interval_hours=1000,hours_since_replacement=700,projected_daily_flight_hours=5,conservative_lead_time_days=20,buffer_days=5,policy_decision='Allowed',expected_need_date='2026-12-11',expected_latest_order_date='2026-11-16',expected_result='Recommend'),
      dict(scenario_id='M-02',aircraft_part_id='AC-02-PC-03',scenario_date='2026-10-12',replacement_interval_hours=1000,hours_since_replacement=990,projected_daily_flight_hours=5,conservative_lead_time_days=20,buffer_days=5,policy_decision='Allowed',expected_need_date='2026-10-14',expected_latest_order_date='2026-09-19',expected_result='Escalate'),
      dict(scenario_id='M-03',aircraft_part_id='AC-03-PC-04',scenario_date='2026-10-12',replacement_interval_hours=1000,hours_since_replacement=700,projected_daily_flight_hours=5,conservative_lead_time_days=20,buffer_days=5,policy_decision='Blocked',expected_need_date='2026-12-11',expected_latest_order_date='2026-11-16',expected_result='Blocked')])
    files={str(f.relative_to(root)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(data.rglob('*.csv'))}
    manifest=dict(dataset_version=VERSION,seed=seed,total_orders=len(orders),aircraft_models=len(aircraft),aircraft_part_associations=len(associations),split_counts={k:len(v) for k,v in splits.items()},excluded_count=len(excluded),train_cutoff=TRAIN_CUTOFF,validation_cutoff=VALIDATION_CUTOFF,observation_end=OBSERVATION_END,feature_columns=FEATURES,target=TARGET,release_scope='Approved fictional classroom training derivative; no operational or restricted real data',sha256=files)
    (data/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ['total_orders','aircraft_models','aircraft_part_associations','split_counts','excluded_count']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--seed',type=int,default=SEED);a=p.parse_args();generate(a.output,a.seed)
