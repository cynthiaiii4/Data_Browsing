import pandas as pd
'''
此class為計算特定區間內的以下資訊
1.該區間首日對應的季報和月報資訊
2.該區間最後一日的價量、籌碼、大盤資訊
3.該區間最後一天收盤價-該區間第一天收盤價的價格變化和變化%
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
        #取得首日價量資訊以及計算 區間最大價差 和 區間最大價差%
        stock_data = self.getFliterStock()
        #取得其他table資料
        m_data = self.m_data
        q_data = self.q_data
        chips_data= self.ch_data
        market_data = self.mk_data

        # 先將相關數據確定轉為日期格式
        m_data['月報所屬日期'] = pd.to_datetime(m_data['月報所屬日期'])
        m_data['營收發布日'] = pd.to_datetime(m_data['營收發布日'])
        q_data['季報所屬日期'] = pd.to_datetime(q_data['季報所屬日期'])
        q_data['季報發布日'] = pd.to_datetime(q_data['季報發布日'])
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

        #調整欄位名稱
        stock_data=self.getNewStockColName(stock_data)
        chips_data=self.getNewChipsColName(chips_data)
        market_data=self.getNewMarketColName(market_data)

        #合併
        final_merged_df = pd.merge(stock_data, m_data, on=['月報所屬日期', '證券代碼'], how='left').merge(q_data, on=['季報所屬日期', '證券代碼'], how='left').merge(chips_data, on=['日期', '證券代碼'], how='left').merge(self.company_data, on=['證券代碼'], how='left').merge(market_data,left_on=['日期', '上市別'], right_on=['日期', '指數名稱'], how='left')
        return final_merged_df

    def getFliterStock(self):

        s_data =self.s_data

        #找出符合條件的公司股價資料
        stock_fliter_data = s_data[(s_data['證券代碼'].isin(self.selected_companies))]

        # 先將 DataFrame 根據 "證券代碼" 和 "日期" 進行排序
        stock_fliter_data = stock_fliter_data.sort_values(by=["證券代碼", "日期"], ascending=[True, True])

        #取得有資料的首日
        first_date = stock_fliter_data.head(1)['日期']

        #取得區間內最高價
        max_prices= stock_fliter_data.groupby('證券代碼')['最高價(元)'].max()
        max_prices = max_prices.rename('區間最高價(元)').reset_index()

        start_prices = stock_fliter_data[stock_fliter_data['日期'] == first_date.iloc[0]]
        result_df = pd.merge(max_prices, start_prices, on='證券代碼', how='left')
        # 計算 "區間最高股價變化"
        result_df['區間最大價差'] = (result_df['區間最高價(元)'] - result_df['最低價(元)'])

        # 計算 "區間最高股價變化率"
        result_df['區間最大股價變化率'] = ((result_df['區間最高價(元)'] - result_df['最低價(元)'])/result_df['最低價(元)']*100).round(2)
        return result_df  
  
    def getNewStockColName(self,stock_data):
        columns_to_add_prefix = ['開盤價(元)', '最高價(元)', '最低價(元)', '收盤價(元)', '成交量(千股)', '5日均價(元)', '10日均價(元)', '20日均價(元)', '60日均價(元)', '5日均量', '10日均量', '20日均量', '60日均量']
        stock_data.rename(columns={col: '分析起日-' + col for col in columns_to_add_prefix}, inplace=True)
        return stock_data

    def getNewChipsColName(self,chips_data):
        columns_to_add_prefix = ['外資買賣超(張)', '投信買賣超(張)', '自營買賣超(張)', '合計買賣超(張)', '外資買賣超日數', '投信買賣超日數', '自營買賣超日數', '法人買賣超日數', '董監持股％', '董監持股數', '融資餘額(張)', '融券餘額(張)', '券資比', '融券增減比率', '融資增減比率', '200-400 張(比率)', '400-600 張(比率)', '600-800 張(比率)', '800-1000張(比率)', '1000張以上 (比率)']
        chips_data.rename(columns={col: '分析起日-' + col for col in columns_to_add_prefix}, inplace=True)
        return chips_data

    def getNewMarketColName(self,market_data):
        columns_to_add_prefix = ['指數開盤價(元)', '指數最高價(元)', '指數最低價(元)', '指數收盤價(元)', '指數成交量(千股)', '指數5日平均點數', '指數10日平均點數', '指數20日平均點數', '指數60日平均點數', '指數5日均量', '指數10日均量', '指數20日均量', '指數60日均量']
        market_data.rename(columns={col: '分析起日-' + col for col in columns_to_add_prefix}, inplace=True)
        return market_data
    