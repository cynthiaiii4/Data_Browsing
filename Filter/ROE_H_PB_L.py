import pandas as pd

def ROE_H_PB_L(q_data,company_data):
    selected_data = pd.DataFrame()
    merged_data = pd.merge(q_data, company_data, on='證券代碼')
    # merged_data
    # 根據證券代碼由小到大，日期由大到小排序
    sorted_data = merged_data.sort_values(by=['證券代碼', '季報所屬日期'], ascending=[True, False])

    # 取每個證券代碼的第一筆數據
    selected_data = sorted_data.groupby('證券代碼').head(1)
    # selected_data

    for industry in selected_data['產業別'].unique():
        industry_data = selected_data[selected_data['產業別'] == industry]

        sorted_data = industry_data.sort_values(by='ROE(A)－稅後', ascending=False)
        
        # 取排序後的前50%數據
        selected_data  = pd.concat([selected_data, sorted_data.head(int(len(sorted_data)*0.3))])

    # 加上當季季底P/B < 1的條件
    condition = (selected_data['當季季底P/B'] < 1)

    # 應用條件篩選
    selected_data = selected_data[condition]

    selected_companies = selected_data['證券代碼'].unique()
    return selected_companies
    