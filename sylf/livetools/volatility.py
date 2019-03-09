# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from livetools.pricing import BSM, Greeks
from livetools import live_config

class history_volatility:
    
    @staticmethod
    def raw_history_volatility(df):
        # close to close volatility        
        # sigma = sqrt(mean(((x(i)-xm)^2))) * 16
        # x(i) = ln(s(i)/s(i-1))
        df = df[['close']].copy()
        df['ret'] = np.log(df['close']) - np.log(df['close'].shift(periods=1))
        for day_len in [5, 15, 30, 50, 60, 70, 90, 120 ,150]:
            df['{}_std'.format(day_len)] = df['ret'].rolling(day_len).std() * 15.8
        del df['close']
        del df['ret']
        return df
    
    @staticmethod
    def Parkinson_history_volatility(df):
        # Parkinson, 1980
        df = df[['high', 'low']].copy()
        df['range'] = (np.log(df['high']) - np.log(df['low']))**2
        for day_len in [5, 15, 30, 50, 60, 70, 90, 120 ,150]:
            df['{}_std'.format(day_len)] = np.sqrt(df['range'].rolling(day_len).mean()/4/(np.log(2))) * 15.8
        del df['range']
        del df['high']
        del df['low']
        return df
    
    @staticmethod
    def GK_history_volatility(df):
        # Garman, Klass, 1980
        pass
    
    @staticmethod
    def RS_history_volatility(df):
        # Rogers, Satchell, 1991
        pass
    
    @staticmethod
    def YZ_history_volatility(df):
        # Yang, Zhang, 2000
        pass

    
    @staticmethod
    def volatility_cone(df):
        hist_vol = history_volatility.raw_history_volatility(df)
        volatility_cone = hist_vol[['5_std','15_std','30_std','50_std','70_std',
                            '90_std','120_std','150_std']].describe().loc[['min','25%','50%','75%','max'],:]
        return volatility_cone
    
class implied_volatility:

    @staticmethod
    def bisection(cp, s, k, t, value):
        value_est = 0
        iv_top = 2 
        iv_floor = 0
        sigma = (iv_floor + iv_top)/2
        iter_num = 0
        while abs(value-value_est) > 1e-8:
            iter_num = iter_num + 1
            if iter_num > 100:
                break
            value_test = BSM.black_scholes(cp, s, k, t, sigma, live_config.RF, live_config.DIV)
            if value - value_test > 0:
                iv_floor = sigma
                sigma = ( sigma + iv_top )/2
            else:
                iv_top = sigma
                sigma = ( sigma + iv_floor )/2
        return sigma    








