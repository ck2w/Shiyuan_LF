# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np

class history_volatility:
    
    @staticmethod
    def raw_history_volatility(df):
        # close to close volatility        
        # sigma = sqrt(mean(((x(i)-xm)^2))) * 16
        # x(i) = ln(s(i)/s(i-1))
        df = df[['close']]
        df['ret'] = np.log(df['close']) - np.log(df['close'].shift(periods=1))
        for day_len in [5, 15, 30, 50, 60, 70, 90, 120 ,150]:
            df['{}_std'.format(day_len)] = df['ret'].rolling(day_len).std() * 15.8
        del df['close']
        del df['ret']
        return df
    
    @staticmethod
    def Parkinson_history_volatility(df):
        # Parkinson, 1980
        df = df[['high', 'low']]
        df['range'] = (np.log(df['high']) - np.log(df['low']))**2
        for day_len in [5, 15, 30, 50, 60, 70, 90, 120 ,150]:
            df['{}_std'.format(day_len)] = np.sqrt(df['range'].rolling(day_len).sum()/4/day_len/(np.log(2))) * 15.8
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


class implied_volatility:
    pass