import pandas as pd
import os
import numpy as np

def DoubleRateRise(file_path,c1,c2):
    data = pd.read_csv(file_path)

    # 設定年份欄位
    data['date'] = pd.to_datetime(data['年月日'])
    data['Year'] = data['date'].dt.year

    selected_data = pd.DataFrame()
    # 找出所有不重複的證券代碼
    unique_companies = data['證券代碼'].unique()
    company_data=data[data['證券代碼'] == unique_companies[0]]

    for company in unique_companies:
        company_data = data[data['證券代碼'] == company]

        recent_data = company_data.head(1)
        # 條件: 最近一筆營收成長率和營業利益率 > 0
        condition2 = (
            (recent_data[c1] > 0) &
            (recent_data[c2] > 0)
        )
        matchcondition_data = recent_data[condition2]
        selected_data = pd.concat([selected_data, matchcondition_data])
   
    # 找出所有符合條件的證券代碼
    selected_companies = selected_data['證券代碼'].unique()
 
    # 計算股價變化
    s_data = data[data['證券代碼'].isin(selected_companies)]
    #把各公司最後一筆-上一筆收盤價
    result = s_data.groupby('證券代碼')['收盤價(元)'].apply(lambda x: x.iloc[0] - x.iloc[1])
    result_df = result.reset_index(name='區間股價變化')
    
    merged_df = pd.merge(selected_data,result_df, on='證券代碼', how='left')
    
    return merged_df

