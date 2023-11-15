import pandas as pd
import os
from Filter.Market import Market

def Higher_Market(s_data,company_data,mk_data,start_d,end_d):
    # 將日期列解析為日期時間對象
    s_data['日期'] = pd.to_datetime(s_data['日期'])

    date_1 = pd.to_datetime(start_d)
    date_2 = pd.to_datetime(end_d)
    filtered_df = s_data[(s_data['日期'] == date_1) | (s_data['日期'] == date_2)]
    filtered_df = filtered_df.sort_values(by=["證券代碼", "日期"], ascending=[True, False])
    filtered_df = pd.merge(filtered_df, company_data, on='證券代碼', how='left')

    price_diff = filtered_df.groupby('證券代碼')['收盤價(元)'].apply(lambda x: x.iloc[0] - x.iloc[1])
    price_diff_percent = filtered_df.groupby('證券代碼')['收盤價(元)'].apply(lambda x: (x.iloc[0] - x.iloc[1])/x.iloc[1])*100
    result_df = pd.DataFrame({
        '證券代碼': price_diff.index,
        '區間股價變化': price_diff.values,
        '區間股價變化率': price_diff_percent.values
    })
    result_df['上市別'] = filtered_df['上市別'].iloc[::2].values
    result_df['區間股價變化'] = result_df['區間股價變化'].round(2)
    result_df['區間股價變化率'] = result_df['區間股價變化率'].round(2)

    #取得大盤表現
    market=Market(mk_data,date_1, date_2)
    #拆分
    tse_df = result_df[result_df['上市別'] == 'TSE']
    otc_df = result_df[result_df['上市別'] == 'OTC']
    #篩選
    tse_filtered = tse_df[tse_df['區間股價變化率'] > market['stock_index_var'].iloc[0]]
    otc_filtered = otc_df[otc_df['區間股價變化率'] > market['otc_var'].iloc[0]]

    filtered_df = pd.concat([tse_filtered, otc_filtered])
    selected_companies=filtered_df['證券代碼'].to_list()

    return selected_companies