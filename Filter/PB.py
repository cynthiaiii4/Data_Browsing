import pandas as pd

def PB(data):
    # data = pd.read_csv(file_path)
    selected_data = pd.DataFrame()
    # 找出所有不重複的證券代碼
    unique_companies = data['證券代碼'].unique()
    company_data=data[data['證券代碼'] == unique_companies[0]]

    for company in unique_companies:
        company_data = data[data['證券代碼'] == company]

        recent_data = company_data.head(1)

        # 條件: 最近一季PB<1
        condition2 = (
            (recent_data['當季季底P/B'] < 1) 
        )
        matchcondition_data = recent_data[condition2]
        selected_data = pd.concat([selected_data, matchcondition_data])
    
    # 找出所有符合條件的證券代碼
    selected_companies = selected_data['證券代碼'].unique()
    return selected_companies
    
    
    # s_data = data[data['證券代碼'].isin(selected_companies)]
    
    #把各公司最後一筆-上一筆收盤價
    # result = s_data.groupby('證期會代碼')['收盤價(元)'].apply(lambda x: x.iloc[0] - x.iloc[1])
    # price_diff = s_data.groupby('證券代碼')['收盤價(元)'].apply(lambda x: x.iloc[0] - x.iloc[1])
    # price_diff_percent = s_data.groupby('證券代碼')['收盤價(元)'].apply(lambda x: (x.iloc[0] - x.iloc[1])/x.iloc[1])*100

    # result_df = pd.DataFrame({
    #     '證券代碼': price_diff.index,
    #     '區間股價變化': price_diff.values,
    #     '區間股價變化率': price_diff_percent.values
    # })

    # result_df['區間股價變化'] = result_df['區間股價變化'].round(2)
    # result_df['區間股價變化率'] = result_df['區間股價變化率'].round(2)

    # merged_df = pd.merge(selected_data,result_df, on='證券代碼', how='left')
    # return merged_df