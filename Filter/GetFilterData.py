import pandas as pd
class GetFilterData:
    def __init__(self, company_data, m_data, q_data, s_data, mk_data, ch_data,selected_companies,start_d,end_d):
        self.company_data = company_data
        self.m_data = m_data
        self.q_data = q_data
        self.s_data = s_data
        self.mk_data = mk_data
        self.ch_data = ch_data
        self.selected_companies = selected_companies
        self.start_d = start_d
        self.end_d = end_d

    def getFliterData(self):
        m_data = self.m_data
        q_data = self.q_data
        # 先將相關數據轉為日期格式
        m_data['月報所屬日期'] = pd.to_datetime(m_data['月報所屬日期'])
        m_data['營收發布日'] = pd.to_datetime(m_data['營收發布日'])
        q_data['季報所屬日期'] = pd.to_datetime(q_data['季報所屬日期'])
        q_data['季報發布日'] = pd.to_datetime(q_data['季報發布日'])
        chips_data= self.getFliterChips()
        market_data = self.getFliterMarket()
        stock_data = self.getFliterStock()
        stock_data['日期'] = pd.to_datetime(stock_data['日期'])
        # m_data 按照 '營收發布日' 以及 q_data 按照 '季報發布日' 從新到舊排序
        m_data = m_data.sort_values(by='營收發布日', ascending=False)
        q_data = q_data.sort_values(by='季報發布日', ascending=False)

        # 查找 '發布日' 對應的 '所屬日期'
        def find_next_date(row, data, date_column, target_date_column):
            company_id = int(row['證券代碼'])
            date = row['日期']
            
            # 從 data 中篩選出相同 '證券代碼' 的紀錄
            correspond_company_data = data[data['證券代碼'] == company_id]
            
            for _, m_row in correspond_company_data.iterrows():
                if date > m_row[date_column]:
                    return m_row[target_date_column]
            
            return None

        # 將 '月報所屬日期' 列填充為對應的 '營收所屬日期'
        stock_data['月報所屬日期'] = stock_data.apply(find_next_date, args=(m_data, '營收發布日', '月報所屬日期',), axis=1)

        # 將 '季報所屬日期' 列填充為對應的 '季報所屬日期'
        stock_data['季報所屬日期'] = stock_data.apply(find_next_date, args=(q_data, '季報發布日', '季報所屬日期',), axis=1)
        final_merged_df = pd.merge(stock_data, m_data, on=['月報所屬日期', '證券代碼'], how='left').merge(q_data, on=['季報所屬日期', '證券代碼'], how='left').merge(chips_data, on=['日期', '證券代碼'], how='left').merge(self.company_data, on=['證券代碼'], how='left').merge(market_data,left_on=['日期', '上市別'], right_on=['日期', '指數名稱'], how='left')
        return final_merged_df

    def getFliterStock(self):

        s_data =self.s_data

        #找出符合條件的公司股價資料
        stock_fliter_data = s_data[(s_data['證券代碼'].isin(self.selected_companies)) & (s_data['日期'] >= self.start_d) & (s_data['日期'] <= self.end_d)]

        # 先將 DataFrame 根據 "證券代碼" 和 "日期" 進行排序
        stock_fliter_data = stock_fliter_data.sort_values(by=["證券代碼", "日期"], ascending=[True, False])

        # 計算 "區間股價變化"
        stock_fliter_data["區間股價變化"] = stock_fliter_data.groupby("證券代碼")["收盤價(元)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)

        # 計算 "區間股價變化率"
        stock_fliter_data["區間股價變化率"] = stock_fliter_data.groupby("證券代碼")["收盤價(元)"].transform(lambda x: (x.iloc[0] - x.iloc[-1]) / x.iloc[-1] * 100).round(2)


        # 選擇每個分組的第一筆資料，包含 "區間股價變化" 和 "區間股價變化率" 欄位
        stock_data = stock_fliter_data.groupby("證券代碼").first().reset_index()
        return stock_data  
    
    def getFliterMarket(self):
        mk_data = self.mk_data
        #找出符合條件的公司指數資料
        mk_fliter_data = mk_data[(mk_data['日期'] >= self.start_d) & (mk_data['日期'] <= self.end_d)]
        # 先將 DataFrame 根據 "證券代碼" 和 "日期" 進行排序
        mk_fliter_data = mk_fliter_data.sort_values(by=["指數名稱", "日期"], ascending=[True, False])

        # 計算 "區間股價變化"
        mk_fliter_data["區間指數變化"] = mk_fliter_data.groupby("指數名稱")["指數收盤價(元)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)

        # 計算 "區間股價變化率"
        mk_fliter_data["區間指數變化率"] = mk_fliter_data.groupby("指數名稱")["指數收盤價(元)"].transform(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[-1] * 100).round(2)

        # 選擇每個分組的第一筆資料，包含 "區間股價變化" 和 "區間股價變化率" 欄位
        market_data = mk_fliter_data.groupby("指數名稱").first().reset_index()

        return market_data 
    
    def getFliterChips(self):
        ch_data = self.ch_data
        #找出符合條件的公司籌碼資料
        ch_fliter_data = ch_data[(ch_data['證券代碼'].isin(self.selected_companies)) & (ch_data['日期'] >= self.start_d) & (ch_data['日期'] <= self.end_d)]
        # 先將 DataFrame 根據 "證券代碼" 和 "日期" 進行排序
        ch_fliter_data = ch_fliter_data.sort_values(by=["證券代碼", "日期"], ascending=[True, False])

        # 計算 各區間變化
        ch_fliter_data["區間董監持股變化"] = ch_fliter_data.groupby("證券代碼")["董監持股數"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
        ch_fliter_data["區間融資餘額(張)變化"] = ch_fliter_data.groupby("證券代碼")["融資餘額(張)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
        ch_fliter_data["區間融券餘額(張)變化"] = ch_fliter_data.groupby("證券代碼")["融券餘額(張)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
        ch_fliter_data["區間200-400 張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["200-400 張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
        ch_fliter_data["區間400-600 張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["400-600 張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
        ch_fliter_data["區間600-800 張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["600-800 張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
        ch_fliter_data["區間800-1000張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["800-1000張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
        ch_fliter_data["區間1000張以上  (比率)變化"] = ch_fliter_data.groupby("證券代碼")["1000張以上  (比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)


        # 定義一個函數計算區間變化率，處理分母為零的情況

        def calculate_change_rate(x):
            if ((x.iloc[-1] == 0 )&(x.iloc[0] != 0)) :
                return 10000  # 如果分母為零，設置為float64的最大值
            return ((x.iloc[-1] - x.iloc[0]) / x.iloc[-1] * 100).round(2)

        # 計算 "區間變化率"
        ch_fliter_data["區間董監持股變化率"] = ch_fliter_data.groupby("證券代碼")["董監持股數"].transform(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[-1] * 100).round(2)
        ch_fliter_data["區間融資餘額(張)變化率"] = ch_fliter_data.groupby("證券代碼")["融資餘額(張)"].transform(calculate_change_rate)
        ch_fliter_data["區間融券餘額(張)變化率"] = ch_fliter_data.groupby("證券代碼")["融券餘額(張)"].transform(calculate_change_rate)
        # 選擇每個分組的第一筆資料，包含 "區間股價變化" 和 "區間股價變化率" 欄位
        chips_data = ch_fliter_data.groupby("證券代碼").first().reset_index()

        return chips_data 
    
