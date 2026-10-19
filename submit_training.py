"""Print a plan by default. --execute uploads two files and starts one paid job."""
import argparse,hashlib,json,re
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def build_request(c,mode,job):
    if any('REPLACE' in str(v) for v in c.values()):raise ValueError('Mentor must fill all config placeholders first.')
    if not re.fullmatch(r'\d{12}',c['expected_account_id']):raise ValueError('Account ID must be 12 digits.')
    if not re.fullmatch(r'arn:aws:iam::'+c['expected_account_id']+r':role/.+',c['execution_role_arn']):raise ValueError('Execution role must belong to the expected account.')
    if not c['prefix'].startswith('capstone/v1/') or '..' in c['prefix']:raise ValueError('Use capstone/v1/<team> as prefix.')
    if not re.fullmatch(c['expected_account_id']+r'\.dkr\.ecr\.'+re.escape(c['region'])+r'\.amazonaws\.com/.+@sha256:[0-9a-f]{64}',c['training_image_uri']):raise ValueError('Use a same-account, same-region ECR image pinned by sha256 digest.')
    if not 60<=int(c['max_runtime_seconds'])<=3600:raise ValueError('Runtime limit must be between 60 and 3600 seconds.')
    if c['instance_type'] not in ['ml.m5.large','ml.m5.xlarge','ml.c5.xlarge']:raise ValueError('Select an approved small CPU instance.')
    if not 5<=int(c['volume_size_gb'])<=30:raise ValueError('Volume size must be 5–30 GB for this starter.')
    prefix=c['prefix'].strip('/')+'/'+mode
    channels=[]
    for split in ['train','validation']:
        channels.append({'ChannelName':split,'DataSource':{'S3DataSource':{'S3DataType':'S3Prefix','S3Uri':f's3://{c["bucket"]}/{prefix}/prepared/{split}/{split}.csv','S3DataDistributionType':'FullyReplicated'}},'ContentType':'text/csv','InputMode':'File'})
    return {'TrainingJobName':job,'AlgorithmSpecification':{'TrainingImage':c['training_image_uri'],'TrainingInputMode':'File'},'RoleArn':c['execution_role_arn'],'InputDataConfig':channels,'OutputDataConfig':{'S3OutputPath':f's3://{c["bucket"]}/{prefix}/runs/'},'ResourceConfig':{'InstanceType':c['instance_type'],'InstanceCount':1,'VolumeSizeInGB':c['volume_size_gb']},'StoppingCondition':{'MaxRuntimeInSeconds':int(c['max_runtime_seconds'])},'EnableNetworkIsolation':True,'Tags':[{'Key':'Project','Value':'ASU-Capstone'},{'Key':'DatasetVersion','Value':'1.0.0'}]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',default=ROOT/'config/aws.json');p.add_argument('--dataset',choices=['smoke','full'],default='smoke');p.add_argument('--execute',action='store_true');a=p.parse_args()
    c=json.loads(Path(a.config).read_text());job='capstone-'+a.dataset+'-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S');request=build_request(c,a.dataset,job);print(json.dumps(request,indent=2))
    if not a.execute:print('PLAN ONLY: no AWS calls, uploads or paid jobs. Add --execute after checking the plan.');raise SystemExit(0)
    import boto3
    session=boto3.Session(region_name=c['region']);identity=session.client('sts').get_caller_identity()
    if identity['Account']!=c['expected_account_id']:raise ValueError('Signed in to the wrong AWS account. Nothing uploaded.')
    s3=session.client('s3');location=s3.get_bucket_location(Bucket=c['bucket'])['LocationConstraint'] or 'us-east-1'
    if location!=c['region']:raise ValueError('Bucket region differs from training region. Nothing uploaded.')
    files={};base='smoke' if a.dataset=='smoke' else 'prepared'
    for split in ['train','validation']:
        local=ROOT/'data'/base/split/(split+'.csv');key=c['prefix'].strip('/')+'/'+a.dataset+'/prepared/'+split+'/'+split+'.csv';s3.upload_file(str(local),c['bucket'],key);files[str(local.relative_to(ROOT))]=hashlib.sha256(local.read_bytes()).hexdigest()
    response=session.client('sagemaker').create_training_job(**request)
    record={'request':request,'response':response['TrainingJobArn'],'submitted_by':identity['Arn'],'data_sha256':files,'dataset':a.dataset}
    out=ROOT/'artifacts/aws';out.mkdir(parents=True,exist_ok=True);(out/(job+'.json')).write_text(json.dumps(record,indent=2)+'\n');print('Started:',job,'\nRecord:',out/(job+'.json'))
