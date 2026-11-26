import numpy as np
import pandas as pd
from pathlib import Path

def generate(root):
    rng = np.random.default_rng(2026)
    root = Path(root); (root/'data').mkdir(exist_ok=True)
    provinces = ['Ontario','Quebec','British Columbia','Alberta','Manitoba']
    customers = pd.DataFrame({'customer_id': [f'C{i:05d}' for i in range(1,5001)], 'province': rng.choice(provinces,5000,p=[.40,.23,.17,.13,.07])})
    months = pd.period_range('2026-01','2026-06',freq='M')
    counts = [15,19,22,27,34,43]
    frames=[]
    for month, cases, size in zip(months,counts,[3333,3333,3333,3333,3334,3334]):
        ids = rng.choice(customers.customer_id,size)
        fraud = np.zeros(size,dtype=int); fraud[rng.choice(size,cases,replace=False)]=1
        amount = np.round(rng.lognormal(6.2,1.0,size),2)
        amount[fraud==1]=np.round(rng.lognormal(7.7,.65,cases),2)
        category = np.full(size,'None',dtype=object)
        category[fraud==1]=rng.choice(['Account takeover','Unauthorized payment','Identity theft'],cases,p=[.45,.35,.20])
        recovery = np.where(fraud==1,np.round(amount*rng.beta(2,6,size),2),0)
        alerts = np.where(fraud==1,rng.random(size)<.74,rng.random(size)<.045).astype(int)
        frames.append(pd.DataFrame({'date': [str(month.start_time.date()+pd.Timedelta(days=int(d))) for d in rng.integers(0,month.days_in_month,size)],'customer_id':ids,'channel':rng.choice(['Mobile','Online','ATM','Branch'],size,p=[.45,.30,.15,.10]),'amount_cad':amount,'confirmed_fraud':fraud,'fraud_category':category,'alert_flag':alerts,'gross_loss_cad':np.where(fraud==1,amount,0),'recovered_cad':recovery}))
    tx=pd.concat(frames,ignore_index=True).sort_values('date').reset_index(drop=True)
    tx.insert(0,'transaction_id',[f'T{i:06d}' for i in range(1,len(tx)+1)])
    tx['net_loss_cad']=(tx.gross_loss_cad-tx.recovered_cad).round(2)
    customers.to_csv(root/'data/customers.csv',index=False); tx.to_csv(root/'data/transactions.csv',index=False)
    return customers,tx
