# -*- coding: utf-8 -*-

import pandas as pd

def days_diff(df):
    for i in range(df.shape[1]):
        df.iloc[:,i] = pd.to_datetime(df.iloc[:,i], format='%Y%m%d')
    return (df.iloc[:,1]-df.iloc[:,0]).dt.days.apply(float)
    
    
    
    