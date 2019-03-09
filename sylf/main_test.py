# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from livetools.pricing import BSM, Greeks
from livetools.volatility import history_volatility, implied_volatility
from livetools import live_config
from livetools import live_utils


def hist_vol():
    equities_data = pd.read_csv(live_config.EQUITIES_DATA).sort_values('trade_date')
    equities_data = equities_data.set_index('trade_date')
    equities_data = equities_data[equities_data.index>20180101]
    
    hist_vol = history_volatility.raw_history_volatility(equities_data)
    # hist_vol = history_volatility.Parkinson_history_volatility(equities_data)
    plt.plot(hist_vol[['30_std', '60_std', '90_std']].values)
    plt.title('hist volatility')
    plt.show()
    
    volatility_cone = history_volatility.volatility_cone(equities_data)
    plt.plot(volatility_cone.T)
    plt.title('volatility cone')
    plt.show()

def imp_vol():
    options_data = pd.read_csv(live_config.OPTIONS_DATA).sort_values('trade_date')
    options_data = options_data[options_data['trade_date']>20190101]
    options_contracts = pd.read_csv(live_config.OPTIONS_CONTRACTS_DATA)[['ts_code', 'per_unit', 'call_put', 'exercise_price', 'maturity_date', 's_month']]
    equities_data = pd.read_csv(live_config.EQUITIES_DATA).sort_values('trade_date')[['trade_date', 'close']].rename(columns={'close': 'equities_close'})
    
    options_data = pd.merge(options_data, options_contracts, how='left', on=['ts_code'])
    options_data = pd.merge(options_data, equities_data, how='left', on=['trade_date'])
    
    options_data['maturity_time'] = live_utils.days_diff(options_data[['trade_date', 'maturity_date']])/live_config.YEAR_DAYS
    options_data['call_put'] = options_data['call_put'].apply(lambda x: 1 if x =='C' else -1)
    
    # pricing test
    options_data['iv'] = 0.1
    options_data['value'] = BSM.black_scholes_df(options_data[['call_put', 'equities_close', 'exercise_price', 'maturity_time', 'iv']])
    options_data['vega'] = Greeks.vega_df(options_data[['call_put', 'equities_close', 'exercise_price', 'maturity_time', 'iv']])
    
    # iv calculation test
    options_data['iv'] = np.nan
    for i in range(options_data.shape[0]):
        print(i/options_data.shape[0])
        sl = options_data.iloc[i,:]
        options_data['iv'].iloc[i] = implied_volatility.bisection(sl['call_put'], sl['equities_close'],sl['exercise_price'],sl['maturity_time'],sl['close'])
    return options_data

options_data = pd.read_csv('bb.csv')

# volatility surface
currentdate = 20190306
maturity_month = [201903, 201904, 201906, 201909]
for s_month in maturity_month:
    ops = options_data[(options_data['trade_date']==currentdate) & (options_data['s_month']==s_month)].sort_values('exercise_price')
    ops['moneyness'] = ops['exercise_price']/ops['equities_close']
#    ops = ops[((ops['moneyness']>=1) & (ops['call_put']==1)) | ((ops['moneyness']<=1) & (ops['call_put']==-1))]
    ops = ops[(ops['call_put']==-1)]
    ops = ops.sort_values('moneyness')    
    ops = ops.set_index('moneyness')
    plt.plot(ops['iv'])
plt.title('iv surface')
plt.show()

