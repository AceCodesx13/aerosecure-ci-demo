"""Same CPU training program for local execution and the provided AWS container."""
import argparse, csv, hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
import joblib, numpy as np, pandas as pd, sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from schema import CATEGORICAL, NUMERIC, FEATURES, TARGET, SEED, VERSION

def metric(y,p):
    y=np.asarray(y);p=np.asarray(p)
    return {'mae_days':round(float(np.mean(np.abs(y-p))),3),'rmse_days':round(float(np.sqrt(np.mean((y-p)**2))),3),'underestimate_rate':round(float(np.mean(p<y)),4)}

def file_in(path,name):
    p=Path(path);return p/name if p.is_dir() else p

def train(train_path,validation_path,model_dir,reports_dir,trees=120):
    tr=pd.read_csv(train_path);va=pd.read_csv(validation_path)
    if list(tr.columns)!=list(va.columns):raise ValueError('Train and validation schemas differ. Run validate_data.py.')
    if not set(FEATURES+[TARGET]).issubset(tr.columns):raise ValueError('Required columns missing.')
    historical=tr.groupby('part_category_id')[TARGET].median().to_dict();fallback=float(tr[TARGET].median())
    pre=ColumnTransformer([('category',Pipeline([('missing',SimpleImputer(strategy='most_frequent')),('encode',OneHotEncoder(handle_unknown='ignore'))]),CATEGORICAL),('numeric',SimpleImputer(strategy='median'),NUMERIC)])
    model=Pipeline([('prepare',pre),('regressor',RandomForestRegressor(n_estimators=trees,max_depth=18,min_samples_leaf=3,random_state=SEED,n_jobs=2))])
    model.fit(tr[FEATURES],tr[TARGET]);pred=np.maximum(1,model.predict(va[FEATURES]))
    # One-sided validation residual quantile, used only as a conservative planning estimate.
    margin=max(0,float(np.quantile(va[TARGET].to_numpy()-pred,0.90,method='higher')))
    median_pred=va['part_category_id'].map(historical).fillna(fallback)
    quoted=va['quoted_lead_time_days'].to_numpy()
    report={'dataset_version':VERSION,'evaluation_split':'validation','row_count':len(va),'quoted_baseline':metric(va[TARGET],quoted),'historical_median_baseline':metric(va[TARGET],median_pred),'model':metric(va[TARGET],pred),'conservative_margin_days':round(margin,3),'validation_coverage':round(float(np.mean(va[TARGET]<=pred+margin)),4),'parameters':{'trees':trees,'max_depth':18,'min_samples_leaf':3,'seed':SEED},'versions':{'python':sys.version.split()[0],'sklearn':sklearn.__version__,'numpy':np.__version__,'pandas':pd.__version__},'inputs':{str(p):hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in [train_path,validation_path]},'created_utc':datetime.now(timezone.utc).isoformat()}
    model_dir=Path(model_dir);reports_dir=Path(reports_dir);model_dir.mkdir(parents=True,exist_ok=True);reports_dir.mkdir(parents=True,exist_ok=True)
    joblib.dump({'pipeline':model,'margin':margin,'historical_medians':historical,'fallback':fallback,'features':FEATURES,'metadata':report},model_dir/'model.joblib')
    (reports_dir/'validation_metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return report

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser()
    p.add_argument('--train',default=os.environ.get('SM_CHANNEL_TRAIN',str(root/'data/prepared/train/train.csv')))
    p.add_argument('--validation',default=os.environ.get('SM_CHANNEL_VALIDATION',str(root/'data/prepared/validation/validation.csv')))
    p.add_argument('--model-dir',default=os.environ.get('SM_MODEL_DIR',str(root/'artifacts/model')))
    p.add_argument('--reports-dir',default=os.environ.get('SM_OUTPUT_DATA_DIR',str(root/'artifacts/reports')))
    p.add_argument('--trees',type=int,default=120);args,_=p.parse_known_args()
    train(file_in(args.train,'train.csv'),file_in(args.validation,'validation.csv'),args.model_dir,args.reports_dir,args.trees)
