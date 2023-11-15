import pandas as pd
import os
import numpy as np
from datetime import datetime

def calculate_var(data, stock_code, day1, day2):
    stock_data = data[data['指數名稱'] == stock_code]

    d1 = pd.to_datetime(day1)
    d2 = pd.to_datetime(day2)
    price1 = stock_data.loc[stock_data['日期'] == d1, '指數收盤價(元)'].values
    price2 = stock_data.loc[stock_data['日期'] == d2, '指數收盤價(元)'].values

    if not price1:
        price1 = stock_data.loc[stock_data['日期'] > d1, '指數收盤價(元)'].values
    if not price2:
        price2 = stock_data.loc[stock_data['日期'] > d2, '指數收盤價(元)'].values
 
    if len(price1) > 0 and len(price2) > 0:
        price1 = price1[0]
        price2 = price2[0]

        if price2 != 0:
            var = (price1 - price2) / price2
        else:
            var = 0  
    else:
        var = 0

    return var

def Market(data,day1, day2):
    # DATA_DIR = ''
    # FILE_NAME = 'v1Stockprice_market.xlsx'
    # data_path = os.path.join(DATA_DIR, FILE_NAME)
    # data = pd.read_excel(data_path)

    stock_index_var = calculate_var(data, 'TSE', day1, day2)
    otc_var = calculate_var(data, 'OTC', day1, day2)

    s_result_df = pd.DataFrame({
            'stock_index_var': stock_index_var,
            'stock_index_increase': np.where(stock_index_var > 0, 1, 0),
            'otc_var': otc_var,
            'otc_var_increase': np.where(otc_var > 0, 1, 0)
        }, index=['row1'])

    return s_result_df
