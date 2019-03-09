# -*- coding: utf-8 -*-


import numpy as np
from scipy import stats
import math
from livetools import live_config

class BSM:
    @staticmethod
    def black_scholes(cp, s, k, t, v, rf, div):
        """ Price an option using the Black-Scholes model.
        s: initial stock price
        k: strike price
        t: expiration time
        v: volatility
        rf: risk-free rate
        div: dividend
        cp: +1/-1 for call/put
        """
        
        d1 = (math.log(s/k)+(rf-div+0.5*math.pow(v,2))*t)/(v*math.sqrt(t))
        d2 = d1 - v*math.sqrt(t)
        
        optprice = (cp*s*math.exp(-div*t)*stats.norm.cdf(cp*d1)) - (cp*k*math.exp(-rf*t)*stats.norm.cdf(cp*d2))
        return optprice
    
    @staticmethod
    def black_scholes_df(df):
        d1 = (np.log(df['equities_close']/df['exercise_price']) +(live_config.RF - live_config.DIV + 0.5*df['iv']**2)) * df['maturity_time'] / (df['iv'] * np.sqrt(df['maturity_time']))
        d2 = d1 - df['iv'] * np.sqrt(df['maturity_time'])        
        value = (df['call_put'] * df['equities_close'] * np.exp(-live_config.DIV*df['maturity_time']) * stats.norm.cdf(df['call_put']*d1)) - (df['call_put'] * df['exercise_price'] * np.exp(-live_config.RF*df['maturity_time']) * stats.norm.cdf(df['call_put']*d2))
        return value
        
class Greeks:
    
    @staticmethod
    def vega_df(df):
        d1 = (np.log(df['equities_close']/df['exercise_price']) +(live_config.RF - live_config.DIV + 0.5*df['iv']**2)) * df['maturity_time'] / (df['iv'] * np.sqrt(df['maturity_time']))
        vega = df['equities_close'] * stats.norm.cdf(d1,0.,1.) * np.sqrt(df['maturity_time'])
        return vega
    