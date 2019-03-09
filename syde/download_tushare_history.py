# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import time
pro = ts.pro_api()

DATA_FOLDER = r'E:\pyworkspace\Shiyuan_LF\sydata\tushare_data\\'

equities_data = []
futures_data = []
options_data = []


option_contracts = pro.opt_basic(exchange='SSE')
option_contracts.to_csv('{}options_contracts.csv'.format(DATA_FOLDER), index=False)

# =============================================================================
# # equities
# for year in range(2010,2020):
#     time.sleep(6)
#     equities_data_year = pro.fund_daily(ts_code='510050.SH', 
#                                    start_date='{}0101'.format(year), 
#                                    end_date='{}1231'.format(year))
#     equities_data.append(equities_data_year)
#     print('equities year = {}'.format(year))
# equities_df = pd.concat(equities_data).sort_values('trade_date')
# equities_df.to_csv('{}equities.csv'.format(DATA_FOLDER), index=False)
# 
# # options
# for i in range(option_contracts.shape[0]):
#     time.sleep(6)
#     ts_code = option_contracts['ts_code'].iloc[i]
#     start_date = option_contracts['list_date'].iloc[i]
#     end_date = option_contracts['delist_date'].iloc[i]
#     option_data_contract = pro.opt_daily(ts_code=ts_code)
#     options_data.append(option_data_contract)
#     print('options contract = {}'.format(ts_code))
# options_df = pd.concat(options_data).sort_values('trade_date')
# options_df.to_csv('{}options.csv'.format(DATA_FOLDER), index=False)
# 
# # futures
# for year in range(10, 20):
#     for month in range(1, 13):
#         time.sleep(6)
#         futures_data_contract = pro.fut_daily(ts_code='IH{}.CFX'.format(year*100+month))
#         futures_data.append(futures_data_contract)
#         print('futures contract = {}'.format(year*100+month))
# futures_df = pd.concat(futures_data).sort_values('trade_date')
# futures_df.to_csv('{}futures.csv'.format(DATA_FOLDER), index=False)
# 
# 
# =============================================================================
