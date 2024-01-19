import pandas as pd
from datetime import datetime

def GetQData(date_str,data):

    # 將日期欄位解析為日期時間對象
    data['季報所屬日期'] = pd.to_datetime(data['季報所屬日期'])
    selected_date = datetime.strptime(date_str, "%Y/%m/%d")

    # 找到符合日期的最後一天（根據您的需求）
    if datetime(selected_date.year, 4, 1)<=selected_date <= datetime(selected_date.year, 5, 15):
        last_day = datetime(selected_date.year-1, 12, 30)
    elif datetime(selected_date.year, 5, 16)<=selected_date <= datetime(selected_date.year, 8, 14):
        last_day = datetime(selected_date.year, 3, 31)
    elif datetime(selected_date.year, 8, 15)<=selected_date <= datetime(selected_date.year, 11, 14):
        last_day = datetime(selected_date.year, 6, 30)
    else:
        last_day = datetime(selected_date.year - 1, 9, 30)

    # 過濾出符合條件的資料
    selected_data = data[data['季報所屬日期'] == last_day]
    return selected_data

def integrate_selected_companies(selected_companies1, selected_companies2):
    # 將兩個列表轉換為集合
    set_selected_companies1 = set(selected_companies1)
    set_selected_companies2 = set(selected_companies2)

    # 取兩者的交集
    integrated_selected_companies = set_selected_companies1.intersection(set_selected_companies2)

    # 將結果轉換為列表
    return list(integrated_selected_companies)

def PB_MA(q_data,start_d,s_data):
    #財報PB<1
    selected_data = pd.DataFrame()
    data=GetQData(start_d,q_data)
    selected_data = data[data['當季季底P/B'] < 1]
    selected_companies1 = selected_data['證券代碼'].unique()

    #收盤>季線
    s_data = s_data.sort_values(by=["證券代碼", "日期"], ascending=[True, True])
   # 按照'證券代碼'分組，並選擇每個分組的第1筆資料
    first_1_records = s_data.groupby('證券代碼').head(1)

    #找出均線多頭排列且股價在所有均線之上
    filtered_df = first_1_records[(first_1_records['收盤價(元)'] > first_1_records['5日均價(元)']) &
               (first_1_records['5日均價(元)'] > first_1_records['10日均價(元)']) &
               (first_1_records['10日均價(元)'] > first_1_records['20日均價(元)'])]

    selected_companies2=filtered_df['證券代碼'].to_list()

    selected_companies = integrate_selected_companies(selected_companies1, selected_companies2)

    return selected_companies
