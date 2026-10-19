import importlib.util,json,sys,unittest
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from policy import can_read,shipment_decision
from policy_demo import recommendation
from schema import FEATURES,TARGET,LABELS
from validate_data import read

class StarterTests(unittest.TestCase):
    def test_access_is_independent_and_defaults_to_denied(self):
        self.assertTrue(can_read('student','Unrestricted'))
        self.assertFalse(can_read('student','Restricted'))
        self.assertTrue(can_read('mentor','Restricted'))
        self.assertFalse(can_read('mentor','Highly Restricted'))
        self.assertTrue(can_read('administrator','Highly Restricted'))
        self.assertFalse(can_read('unknown','Unrestricted'))
        self.assertFalse(can_read('administrator','unknown'))
    def test_blocked_destination_cannot_be_overridden(self):
        for label in LABELS:self.assertEqual(shipment_decision(label,False,'Approved after review')[0],'Blocked')
    def test_authorization_expiry_and_review(self):
        for status in ['Missing','Expired','Valid']:
            self.assertEqual(shipment_decision('Highly Restricted',True,status)[0],'Review required')
        for status in ['Missing','Expired']:
            self.assertEqual(shipment_decision('Restricted',True,status)[0],'Review required')
        self.assertEqual(shipment_decision('Restricted',True,'Valid')[0],'Allowed')
        self.assertEqual(shipment_decision('Highly Restricted',True,'Approved after review')[0],'Allowed')
        self.assertEqual(shipment_decision('Unknown',True,'Valid')[0],'Review required')
        self.assertEqual(shipment_decision('Unrestricted',None,'Not required')[0],'Review required')
    def test_policy_scenario_matrix(self):
        matrix={(r['shipment_restriction_classification'],r['destination_region_id']):r['destination_eligible']=='True' for r in read(ROOT/'data/reference/shipment_policy.csv')}
        for r in read(ROOT/'data/examples/policy_scenarios.csv'):
            self.assertEqual(shipment_decision(r['shipment_restriction_classification'],matrix.get((r['shipment_restriction_classification'],r['destination_region_id'])),r['authorization_status'])[0],r['expected_decision'])
    def test_maintenance_results_and_invalid_usage(self):
        self.assertEqual(recommendation('2026-10-12',1000,700,5,20,5,'Allowed'),('2026-12-11','2026-11-16','Recommend'))
        self.assertEqual(recommendation('2026-10-12',1000,990,5,20,5,'Allowed')[2],'Escalate')
        self.assertEqual(recommendation('2026-10-12',1000,700,5,20,5,'Blocked')[2],'Blocked')
        with self.assertRaises(ValueError):recommendation('2026-10-12',1000,700,0,20,5,'Allowed')
    def test_future_fields_are_not_features(self):
        forbidden={TARGET,'usable_receipt_date','accepted_date','order_id','authorization_status_at_acceptance','data_access_classification','shipment_restriction_classification'}
        self.assertFalse(set(FEATURES)&forbidden)
        self.assertEqual(len(FEATURES),13)
    def test_cloud_plan_omits_test_and_raw(self):
        spec=importlib.util.spec_from_file_location('submit',ROOT/'aws/submit_training.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        c=dict(region='us-east-1',expected_account_id='123456789012',bucket='fictional-test-bucket',prefix='capstone/v1/test-team',execution_role_arn='arn:aws:iam::123456789012:role/TestRole',training_image_uri='123456789012.dkr.ecr.us-east-1.amazonaws.com/capstone@sha256:'+'a'*64,instance_type='ml.m5.large',max_runtime_seconds=1800,volume_size_gb=10)
        req=m.build_request(c,'smoke','capstone-smoke-test');serialized=json.dumps(req)
        self.assertEqual([x['ChannelName'] for x in req['InputDataConfig']],['train','validation'])
        self.assertNotIn('/raw/',serialized);self.assertNotIn('/test/',serialized);self.assertTrue(req['EnableNetworkIsolation'])
        self.assertEqual(req['ResourceConfig']['InstanceCount'],1)
        c['training_image_uri']=c['training_image_uri'].replace('@sha256:'+'a'*64,':latest')
        with self.assertRaises(ValueError):m.build_request(c,'full','capstone-full-test')

if __name__=='__main__':unittest.main()
