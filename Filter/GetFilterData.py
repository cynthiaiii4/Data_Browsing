import pandas as pd
import numpy as np
'''
此class為整合及計算特定區間內的以下資訊
1.該區間首日對應的季報和月報資訊
2.該區間"最高價"當日的價量、籌碼、大盤資訊
3.該區間"最高價"-該區間第一天"最低價"的價格變化和變化%
4.公司基本資料
'''
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
        stock_fliter_data = [(self.s_data['證券代碼'].isin(self.selected_companies)) & (self.s_data['日期'] >= self.start_d) & (self.s_data['日期'] <= self.start_d)]
        stock_fliter_data = self.s_data[(self.s_data['證券代碼'].isin(self.selected_companies)) ]
        stock_fliter_data = stock_fliter_data.sort_values(by="日期", ascending=True)
        #取得分析首日,也就是開始日後第一個有資料的日期
        first_date = stock_fliter_data.head(1)['日期']
        #取得最高價當日的價量資訊
        max_prices_idx = stock_fliter_data.groupby('證券代碼')['最高價(元)'].idxmax()
        max_prices_with_dates = stock_fliter_data.loc[max_prices_idx]
        #取得分析首日的最低價
        start_prices = stock_fliter_data[stock_fliter_data['日期'] == first_date.iloc[0]][['證券代碼', '最低價(元)']]
        result_df = pd.merge(max_prices_with_dates[['證券代碼', '最高價(元)']], start_prices, on='證券代碼', how='left')
        # 計算 "區間最高股價變化"
        result_df['區間股價變化(最高價)'] = (result_df['最高價(元)'] - result_df['最低價(元)'])

        # 計算 "區間最高股價變化率"
        result_df['區間股價變化率(最高價)'] = ((result_df['最高價(元)'] - result_df['最低價(元)'])/result_df['最低價(元)']*100).round(2)
        stock_data = pd.merge(max_prices_with_dates, result_df[['證券代碼','區間股價變化(最高價)','區間股價變化率(最高價)']], on='證券代碼', how='left')
        stock_data.columns = ['最高價當日-' + col if col in ['開盤價(元)', '最高價(元)', '最低價(元)', '收盤價(元)', '成交量(千股)', '5日均價(元)', '10日均價(元)', '20日均價(元)', '60日均價(元)', '5日均量', '10日均量', '20日均量', '60日均量'] else col for col in stock_data.columns]
        #整合最高價當日價量和公司基本資訊
        filter_stock_data=pd.merge(stock_data,self.company_data,on=['證券代碼'], how='left')
        #取得最高價當日大盤狀況
        max_price_mkdata= pd.merge(filter_stock_data,self.mk_data,how='inner', left_on=['日期', '上市別'], right_on=['日期', '指數名稱'])
        max_price_mkdata.columns = ['最高價當日-' + col if col in ['指數開盤價(元)', '指數最高價(元)', '指數最低價(元)', '指數收盤價(元)', '指數成交量(千股)', '指數5日均價(元)', '指數10日均價(元)', '指數20日均價(元)', '指數60日均價(元)', '指數5日均量', '指數10日均量', '指數20日均量', '指數60日均量'] else col for col in max_price_mkdata.columns]
        #找出時間時間條件內的第一日的大盤狀況
        first_date_mdata=self.mk_data[self.mk_data['日期']==first_date.iloc[0]]
        #計算每支股票最高價當日和分析首日的大盤變化
        computed_mkdata = pd.merge(
            max_price_mkdata[['證券代碼', '最高價當日-指數收盤價(元)', '指數名稱']],
            first_date_mdata[['指數收盤價(元)', '指數名稱']],
            on='指數名稱',
            how='left'
        )
        computed_mkdata['最高價當日指數變化']=(computed_mkdata['最高價當日-指數收盤價(元)'] - computed_mkdata['指數收盤價(元)']).round(2)
        computed_mkdata['最高價當日指數變化率']=((computed_mkdata['最高價當日-指數收盤價(元)'] - computed_mkdata['指數收盤價(元)'])/computed_mkdata['指數收盤價(元)']*100).round(2)
        #整合價量、公司資料、大盤
        flited_data_sm=pd.merge(max_price_mkdata,computed_mkdata[['證券代碼','最高價當日指數變化','最高價當日指數變化率']],on='證券代碼',how='left')
        #取得最高價當日籌碼資訊
        max_price_chdata= pd.merge(flited_data_sm,self.ch_data, on=['日期', '證券代碼'],how='inner')
        max_price_chdata.to_excel('max_price_chdata.xlsx', index=False,encoding='UTF-8')
        max_price_chdata.columns = ['最高價當日-' + col if col in ['外資買賣超(張)',
        '投信買賣超(張)',
        '自營買賣超(張)',
        '合計買賣超(張)',
        '外資買賣超日數',
        '投信買賣超日數',
        '自營買賣超日數',
        '法人買賣超日數',	
        '董監持股％',
        '董監持股數',
        '融資餘額(張)',	
        '融券餘額(張)',	
        '券資比',
        '融券增減比率',	
        '融資增減比率',	
        '200-400 張(比率)',	
        '400-600 張(比率)',	
        '600-800 張(比率)',	
        '800-1000張(比率)',	
        '1000張以上(比率)'] else col for col in max_price_chdata.columns]
        #找出時間時間條件內的第一日的籌碼狀況
        first_date_chdata=self.ch_data[self.ch_data['日期']==first_date.iloc[0]]
        #計算最高價當日籌碼和分析首日變化
        computed_chdata = pd.merge(
            max_price_chdata[['證券代碼','最高價當日-董監持股數','最高價當日-融資餘額(張)','最高價當日-融券餘額(張)','最高價當日-200-400 張(比率)','最高價當日-400-600 張(比率)','最高價當日-600-800 張(比率)','最高價當日-800-1000張(比率)','最高價當日-1000張以上(比率)']],
            first_date_chdata[['證券代碼', '董監持股數','融資餘額(張)','融券餘額(張)','200-400 張(比率)','400-600 張(比率)','600-800 張(比率)','800-1000張(比率)','1000張以上(比率)']],
            on='證券代碼',
            how='left'
        )
        computed_chdata['最高價當日董監持股變化']=(computed_chdata['最高價當日-董監持股數'] - computed_chdata['董監持股數']).round(2)
        computed_chdata['最高價當日融資餘額(張)變化']=(computed_chdata['最高價當日-融資餘額(張)'] - computed_chdata['融資餘額(張)']).round(2)
        computed_chdata['最高價當日融券餘額(張)變化']=(computed_chdata['最高價當日-融券餘額(張)'] - computed_chdata['融券餘額(張)']).round(2)
        computed_chdata['最高價當日200-400 張(比率)變化']=(computed_chdata['最高價當日-200-400 張(比率)'] - computed_chdata['200-400 張(比率)']).round(2)
        computed_chdata['最高價當日400-600 張(比率)變化']=(computed_chdata['最高價當日-400-600 張(比率)'] - computed_chdata['400-600 張(比率)']).round(2)
        computed_chdata['最高價當日600-800 張(比率)變化']=(computed_chdata['最高價當日-600-800 張(比率)'] - computed_chdata['600-800 張(比率)']).round(2)
        computed_chdata['最高價當日800-1000張(比率)變化']=(computed_chdata['最高價當日-800-1000張(比率)'] - computed_chdata['800-1000張(比率)']).round(2)
        computed_chdata['最高價當日1000張以上(比率)變化']=(computed_chdata['最高價當日-1000張以上(比率)'] - computed_chdata['1000張以上(比率)']).round(2)


        computed_chdata['最高價當日董監持股變化率']=((computed_chdata['最高價當日-董監持股數'] - computed_chdata['董監持股數'])/computed_chdata['董監持股數']*100).round(2)
        computed_chdata['最高價當日融資餘額(張)變化率'] = np.where(
            computed_chdata['融資餘額(張)'] == 0,  # 分母為0的情況
            0,  # 當分母為0時，將結果設為0
            ((computed_chdata['最高價當日-融資餘額(張)'] - computed_chdata['融資餘額(張)']) / computed_chdata['融資餘額(張)'] * 100).round(2)
        )
        computed_chdata['最高價當日融券餘額(張)變化率'] = np.where(
            computed_chdata['融券餘額(張)'] == 0,  # 分母為0的情況
            0,  # 當分母為0時，將結果設為0
            ((computed_chdata['最高價當日-融券餘額(張)'] - computed_chdata['融券餘額(張)']) / computed_chdata['融券餘額(張)'] * 100).round(2)
        )
        computed_chdata.to_excel('computed_chdata.xlsx', index=False,encoding='UTF-8')
        #整合價量、公司資料、大盤、籌碼、首日日期
        flited_data_smc=pd.merge(max_price_chdata,computed_chdata[['證券代碼','最高價當日董監持股變化','最高價當日融資餘額(張)變化','最高價當日融券餘額(張)變化','最高價當日200-400 張(比率)變化','最高價當日400-600 張(比率)變化','最高價當日600-800 張(比率)變化','最高價當日800-1000張(比率)變化','最高價當日1000張以上(比率)變化','最高價當日董監持股變化率','最高價當日融資餘額(張)變化率','最高價當日融券餘額(張)變化率']],on='證券代碼',how='left')
        flited_data_smc['分析首日']=first_date.iloc[0]
        flited_data_smc = flited_data_smc.rename(columns={'日期': '最高價日期'})
        #整合季報和月報,用分析首日的日期找到對應的資訊
        m_data = self.m_data
        q_data = self.q_data
        m_data['月報所屬日期'] = pd.to_datetime(m_data['月報所屬日期'])
        m_data['營收發布日'] = pd.to_datetime(m_data['營收發布日'])
        q_data['季報所屬日期'] = pd.to_datetime(q_data['季報所屬日期'])
        q_data['季報發布日'] = pd.to_datetime(q_data['季報發布日'])
        flited_data_smc['分析首日'] = pd.to_datetime(flited_data_smc['分析首日'])
        m_data = m_data.sort_values(by='營收發布日', ascending=False)
        q_data = q_data.sort_values(by='季報發布日', ascending=False)
        def find_next_date(row, data, date_column, target_date_column):
            company_id = int(row['證券代碼'])
            date = row['分析首日']
            
            # 從 data 中篩選出相同 '證券代碼' 的紀錄
            correspond_company_data = data[data['證券代碼'] == company_id]
            
            for _, m_row in correspond_company_data.iterrows():
                if date > m_row[date_column]:
                    return m_row[target_date_column]
            
            return None

        # 將 '月報所屬日期' 列填充為對應的 '營收所屬日期'
        flited_data_smc['月報所屬日期'] = flited_data_smc.apply(find_next_date, args=(m_data, '營收發布日', '月報所屬日期',), axis=1)

        # 將 '季報所屬日期' 列填充為對應的 '季報所屬日期'
        flited_data_smc['季報所屬日期'] = flited_data_smc.apply(find_next_date, args=(q_data, '季報發布日', '季報所屬日期',), axis=1)
        final_merged_df = pd.merge(flited_data_smc, m_data, on=['月報所屬日期', '證券代碼'], how='left').merge(q_data, on=['季報所屬日期', '證券代碼'], how='left')
        return final_merged_df
    # def getFliterData(self):
    #     m_data = self.m_data
    #     q_data = self.q_data
    #     # 先將相關數據轉為日期格式
    #     m_data['月報所屬日期'] = pd.to_datetime(m_data['月報所屬日期'])
    #     m_data['營收發布日'] = pd.to_datetime(m_data['營收發布日'])
    #     q_data['季報所屬日期'] = pd.to_datetime(q_data['季報所屬日期'])
    #     q_data['季報發布日'] = pd.to_datetime(q_data['季報發布日'])
    #     #取得最高價日期
    #     self.max_prices_stock = self.getMaxPriceStock()
    #     #取得價量資訊並整合公司資料
    #     stock_data = self.getFliterStock()
    #     filter_stock_data=pd.merge(stock_data,self.company_data,on=['證券代碼'], how='left')
    #     #
    #     chips_data= self.getFliterChips()
    #     market_data = self.getFliterMarket(filter_stock_data)
        
    #     stock_data['日期'] = pd.to_datetime(stock_data['日期'])
    #     # m_data 按照 '營收發布日' 以及 q_data 按照 '季報發布日' 從新到舊排序
    #     m_data = m_data.sort_values(by='營收發布日', ascending=False)
    #     q_data = q_data.sort_values(by='季報發布日', ascending=False)

    #     # 查找 '發布日' 對應的 '所屬日期'
    #     def find_next_date(row, data, date_column, target_date_column):
    #         company_id = int(row['證券代碼'])
    #         date = row['日期']
            
    #         # 從 data 中篩選出相同 '證券代碼' 的紀錄
    #         correspond_company_data = data[data['證券代碼'] == company_id]
            
    #         for _, m_row in correspond_company_data.iterrows():
    #             if date > m_row[date_column]:
    #                 return m_row[target_date_column]
            
    #         return None

    #     # 將 '月報所屬日期' 列填充為對應的 '營收所屬日期'
    #     stock_data['月報所屬日期'] = stock_data.apply(find_next_date, args=(m_data, '營收發布日', '月報所屬日期',), axis=1)

    #     # 將 '季報所屬日期' 列填充為對應的 '季報所屬日期'
    #     stock_data['季報所屬日期'] = stock_data.apply(find_next_date, args=(q_data, '季報發布日', '季報所屬日期',), axis=1)
    #     final_merged_df = pd.merge(stock_data, m_data, on=['月報所屬日期', '證券代碼'], how='left').merge(q_data, on=['季報所屬日期', '證券代碼'], how='left').merge(chips_data, on=['日期', '證券代碼'], how='left').merge(self.company_data, on=['證券代碼'], how='left').merge(market_data,left_on=['日期', '上市別'], right_on=['日期', '指數名稱'], how='left')
    #     return final_merged_df
    
    # def getMaxPriceStock(self):
    #     s_data =self.s_data
    #     stock_fliter_data = [(s_data['證券代碼'].isin(self.selected_companies)) & (s_data['日期'] >= self.start_d) & (s_data['日期'] <= self.end_d)]
    #     max_prices_idx = stock_fliter_data.groupby('證券代碼')['最高價(元)'].idxmax()
    #     max_prices_stock = stock_fliter_data.loc[max_prices_idx]
    #     return max_prices_stock

    # def getFliterStock(self):

    #     s_data =self.s_data

    #     #找出符合條件的公司股價資料
    #     stock_fliter_data = [(s_data['證券代碼'].isin(self.selected_companies)) & (s_data['日期'] >= self.start_d) & (s_data['日期'] <= self.end_d)]

    #     #整合該股票區間內最高價和第一日最低價資訊
    #     start_prices = stock_fliter_data[stock_fliter_data['日期'] == self.start_d][['證券代碼', '最低價(元)']]
    #     result_df = pd.merge(self.max_prices_stock[['證券代碼', '最高價(元)']], start_prices, on='證券代碼', how='left')

    #     # 計算 "區間最高股價變化"
    #     result_df['區間最大價差'] = (result_df['最高價(元)'] - result_df['收盤價(元)']).round(2)

    #     # 計算 "區間最高股價變化率"
    #     result_df['區間最大價差%'] = ((result_df['最高價(元)'] - result_df['收盤價(元)'])/result_df['最低價(元)']*100).round(2)

    #     #取得最高價日期的當天股價狀況並合併計算結果
    #     stock_data = pd.merge(self.max_prices_with_dates, result_df[['證券代碼','區間最大價差','區間最大價差%']], on='證券代碼', how='left')
    #     #換名稱避免誤會
    #     stock_data.columns = ['最高價當日-' + col if col in ['開盤價(元)', '最高價(元)', '最低價(元)', '收盤價(元)', '成交量(千股)', '5日均價(元)', '10日均價(元)', '20日均價(元)', '60日均價(元)', '5日均量', '10日均量', '20日均量', '60日均量'] else col for col in stock_data.columns]
    #     return stock_data   
    
    # def getFliterMarket(self,filter_stock_data):
    #     mk_data = self.mk_data

    #     max_price_mdata= pd.merge(filter_stock_data,mk_data,on=['證券代碼'], how='left')
    #     #找出時間內的資料
    #     mk_fliter_data = mk_data[(mk_data['日期'] >= self.start_d) & (mk_data['日期'] <= self.end_d)]
    #     #排序by日期
    #     mk_fliter_data = mk_fliter_data.sort_values(by="日期", ascending=True)
       
    #     #找出時間條件內的第一日的大盤狀況
    #     first_date_mdata = mk_fliter_data[mk_fliter_data['index_name'] == 'OTC'].head(1)







    #     #********
    #     #找出符合條件的公司指數資料
    #     mk_fliter_data = mk_data[(mk_data['日期'] >= self.start_d) & (mk_data['日期'] <= self.end_d)]
    #     # 先將 DataFrame 根據 "證券代碼" 和 "日期" 進行排序
    #     mk_fliter_data = mk_fliter_data.sort_values(by=["指數名稱", "日期"], ascending=[True, False])

    #     # 計算 "區間股價變化"
    #     mk_fliter_data["區間指數變化"] = mk_fliter_data.groupby("指數名稱")["指數收盤價(元)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)

    #     # 計算 "區間股價變化率"
    #     mk_fliter_data["區間指數變化率"] = mk_fliter_data.groupby("指數名稱")["指數收盤價(元)"].transform(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[-1] * 100).round(2)

    #     # 選擇每個分組的第一筆資料，包含 "區間股價變化" 和 "區間股價變化率" 欄位
    #     market_data = mk_fliter_data.groupby("指數名稱").first().reset_index()

    #     return market_data 
    
    # def getFliterChips(self):
    #     ch_data = self.ch_data
    #     #找出符合條件的公司籌碼資料
    #     ch_fliter_data = ch_data[(ch_data['證券代碼'].isin(self.selected_companies)) & (ch_data['日期'] >= self.start_d) & (ch_data['日期'] <= self.end_d)]
    #     # 先將 DataFrame 根據 "證券代碼" 和 "日期" 進行排序
    #     ch_fliter_data = ch_fliter_data.sort_values(by=["證券代碼", "日期"], ascending=[True, False])

    #     # 計算 各區間變化
    #     ch_fliter_data["區間董監持股變化"] = ch_fliter_data.groupby("證券代碼")["董監持股數"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
    #     ch_fliter_data["區間融資餘額(張)變化"] = ch_fliter_data.groupby("證券代碼")["融資餘額(張)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
    #     ch_fliter_data["區間融券餘額(張)變化"] = ch_fliter_data.groupby("證券代碼")["融券餘額(張)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
    #     ch_fliter_data["區間200-400 張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["200-400 張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
    #     ch_fliter_data["區間400-600 張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["400-600 張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
    #     ch_fliter_data["區間600-800 張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["600-800 張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
    #     ch_fliter_data["區間800-1000張(比率)變化"] = ch_fliter_data.groupby("證券代碼")["800-1000張(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)
    #     ch_fliter_data["區間1000張以上(比率)變化"] = ch_fliter_data.groupby("證券代碼")["1000張以上(比率)"].transform(lambda x: x.iloc[0] - x.iloc[-1]).round(2)


    #     # 定義一個函數計算區間變化率，處理分母為零的情況

    #     def calculate_change_rate(x):
    #         if ((x.iloc[-1] == 0 )&(x.iloc[0] != 0)) :
    #             return 10000  # 如果分母為零，設置為float64的最大值
    #         return ((x.iloc[-1] - x.iloc[0]) / x.iloc[-1] * 100).round(2)

    #     # 計算 "區間變化率"
    #     ch_fliter_data["區間董監持股變化率"] = ch_fliter_data.groupby("證券代碼")["董監持股數"].transform(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[-1] * 100).round(2)
    #     ch_fliter_data["區間融資餘額(張)變化率"] = ch_fliter_data.groupby("證券代碼")["融資餘額(張)"].transform(calculate_change_rate)
    #     ch_fliter_data["區間融券餘額(張)變化率"] = ch_fliter_data.groupby("證券代碼")["融券餘額(張)"].transform(calculate_change_rate)
    #     # 選擇每個分組的第一筆資料，包含 "區間股價變化" 和 "區間股價變化率" 欄位
    #     chips_data = ch_fliter_data.groupby("證券代碼").first().reset_index()

    #     return chips_data 
    
