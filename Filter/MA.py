import pandas as pd

def MA(s_data):
   s_data = s_data.sort_values(by=["證券代碼", "日期"], ascending=[True, False])
   # 按照'證券代碼'分組，並選擇每個分組的最後1筆資料
   last_1_records = s_data.groupby('證券代碼').head(1)

   #找出均線多頭排列且股價在所有均線之上
   filtered_df = last_1_records[(last_1_records['收盤價(元)'] > last_1_records['5日均價(元)']) &
               (last_1_records['5日均價(元)'] > last_1_records['10日均價(元)']) &
               (last_1_records['10日均價(元)'] > last_1_records['20日均價(元)']) &
               (last_1_records['成交量(千股)'] > 3000)]
   selected_companies=filtered_df['證券代碼'].to_list()

   return selected_companies