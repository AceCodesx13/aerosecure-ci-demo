import argparse
from pathlib import Path
import joblib,numpy as np,pandas as pd
from schema import FEATURES

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--model',default=root/'artifacts/model/model.joblib');p.add_argument('--input',default=root/'data/examples/new_orders.csv');p.add_argument('--output',default=root/'artifacts/predictions.csv');a=p.parse_args()
    b=joblib.load(a.model);df=pd.read_csv(a.input);missing=set(FEATURES)-set(df.columns)
    if missing:raise ValueError('Missing input columns: '+str(sorted(missing)))
    pred=np.maximum(1,b['pipeline'].predict(df[FEATURES]));out=df[['order_id']].copy();out['predicted_delivery_days']=np.round(pred,2);out['conservative_delivery_days']=np.ceil(pred+b['margin']).astype(int)
    Path(a.output).parent.mkdir(parents=True,exist_ok=True);out.to_csv(a.output,index=False);print(out.to_string(index=False))
