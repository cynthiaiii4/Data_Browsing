import pandas as pd
from datetime import datetime

def GetQData(date_str,data):

    # 將日期欄位解析為日期時間對象
    data['年月日'] = pd.to_datetime(data['年月日'])
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
    selected_data = data[(data['年月日'] <= last_day) & (data['年月日'] >= (last_day - pd.DateOffset(days=365)))]
    return selected_data
