"""Deterministic policy and maintenance examples, separate from model fitting."""
import math
from datetime import date,timedelta
from pathlib import Path
from validate_data import read
from policy import shipment_decision,can_read

def recommendation(scenario_date,interval,hours,usage,lead,buffer,policy):
    if usage<=0 or interval<=0 or hours<0 or lead<0 or buffer<0:raise ValueError('Invalid maintenance scenario values')
    start=date.fromisoformat(scenario_date);need=start+timedelta(days=math.ceil(max(0,interval-hours)/usage));latest=need-timedelta(days=math.ceil(lead+buffer))
    result='Blocked' if policy=='Blocked' else 'Review required' if policy!='Allowed' else 'Escalate' if latest<start else 'Recommend'
    return need.isoformat(),latest.isoformat(),result

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];matrix={(r['shipment_restriction_classification'],r['destination_region_id']):r['destination_eligible']=='True' for r in read(root/'data/reference/shipment_policy.csv')}
    for r in read(root/'data/examples/policy_scenarios.csv'):
        actual,reason=shipment_decision(r['shipment_restriction_classification'],matrix.get((r['shipment_restriction_classification'],r['destination_region_id'])),r['authorization_status']);assert actual==r['expected_decision'];print(r['scenario_id'],actual,':',reason)
    for r in read(root/'data/examples/maintenance_scenarios.csv'):
        answer=recommendation(r['scenario_date'],float(r['replacement_interval_hours']),float(r['hours_since_replacement']),float(r['projected_daily_flight_hours']),float(r['conservative_lead_time_days']),float(r['buffer_days']),r['policy_decision']);assert answer==(r['expected_need_date'],r['expected_latest_order_date'],r['expected_result']);print(r['scenario_id'],answer)
    print('Student can read Unrestricted:',can_read('student','Unrestricted'))
    print('Student can read Highly Restricted:',can_read('student','Highly Restricted'))
    print('PASS: 9 shipment cases, 3 maintenance cases and access examples. Local simulation only.')
