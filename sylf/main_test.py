# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

from livetools import pricing, volatility
from livetools.volatility import history_volatility
from livetools import live_config



# historical volatility
equities_data = pd.read_csv(live_config.EQUITIES_DATA).sort_values('trade_date')
equities_data = equities_data.set_index('trade_date')
equities_data = equities_data[equities_data.index>20180101]

# hist_vol = history_volatility.raw_history_volatility(equities_data)
hist_vol = history_volatility.Parkinson_history_volatility(equities_data)
# plt.plot(hist_vol[['30_std', '60_std', '90_std']].values)

volatility_cone = hist_vol[['5_std','15_std','30_std','50_std','70_std',
                            '90_std','120_std','150_std']].describe().loc[['min','25%','50%','75%','max'],:]
                            


plt.plot(volatility_cone.T)