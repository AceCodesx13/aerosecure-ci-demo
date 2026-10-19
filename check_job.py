import argparse,json
from pathlib import Path
import boto3
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('job_name');p.add_argument('--config',default=ROOT/'config/aws.json');p.add_argument('--stop',action='store_true');a=p.parse_args();c=json.loads(Path(a.config).read_text());s=boto3.Session(region_name=c['region'])
    if s.client('sts').get_caller_identity()['Account']!=c['expected_account_id']:raise ValueError('Wrong AWS account')
    if not a.job_name.startswith('capstone-'):raise ValueError('Expected a capstone job name')
    client=s.client('sagemaker')
    if a.stop:client.stop_training_job(TrainingJobName=a.job_name)
    job=client.describe_training_job(TrainingJobName=a.job_name);print(json.dumps({k:job[k] for k in ['TrainingJobName','TrainingJobStatus','SecondaryStatus','FailureReason','ModelArtifacts'] if k in job},indent=2,default=str))
