from database import Database
# import talib
import pandas as pd
import numpy as np

# Abstract API：
# from talib import abstract


class Data:
    # 物件初始化: 接收SQL下來DB的資料
    def __init__(self):
        # 與資料庫連線 & 下載全部資料(from database)
        self.db = Database()
        # 初始化stock price 資料
        self.raw_price_data = self.db.get_daily_stock()
        self.all_price_dict = self.handle_price_data()
        # 初始化stock price 資料
        self.raw_report_data = self.db.get_finance_report()

    # """
    # INPUT: self, dataset(str)帶入想要的資料名稱Ex. price:close、report:roe
    # OUTPUT: 一個內容為所有公司股價/財報相關資料的Dataframe
    # FUNCTION: 從DB中取得資料
    # """

    # # 取得資料起點
    # def get(self, dataset):
    #     # 使用 lower() 方法將字串轉換為小寫
    #     dataset = dataset.lower()
    #     # 使用 split() 函數按 ":" 分隔字串
    #     parts = dataset.split(":")
    #     if len(parts) == 2:
    #         subject = parts[0]
    #         item = parts[1]
    #     else:
    #         print("輸入格式錯誤(Ex. price:close)")

    #     if subject == "price":
    #         # 呼叫處理開高低收的FUNCT
    #         price_data = self.all_price_dict[item]
    #         return price_data
    #     elif subject == "report":
    #         # 財報資料的Header為大寫
    #         item = item.upper().replace(" ", "")
    #         # 可能會有多個財報資料，以逗號加空格為分隔符
    #         # 將字串以逗號加空格為分隔符，分割成元素列表
    #         elements = item.split(",")
    #         # 創建一個以元素為鍵，空字串為值的字典
    #         element_dict = {element: "" for element in elements}
    #         # 使用迴圈遍歷字典的鍵值對
    #         for key, value in element_dict.items():
    #             # 呼叫處理財報的FUNCT
    #             element_dict[key] = self.format_report_data(key)

    #         # 有多個財報資料時，回傳一個字典
    #         return element_dict
    #     else:
    #         print("目前資料來源有price、report")

    # # 處理stock price的functions
    # def handle_price_data(self):
    #     self.all_open = self.format_price_data("open")
    #     self.all_high = self.format_price_data("high")
    #     self.all_low = self.format_price_data("low")
    #     self.all_close = self.format_price_data("close")
    #     self.all_volume = self.format_price_data("volume")
    #     self.all_market_capital = self.format_price_data("market_capital")
    #     # 宣告一個字典存放這些dataframe
    #     # 呼叫.indicator時，就是傳入這個dict
    #     self.all_price_dict = {
    #         "open": self.all_open,
    #         "high": self.all_high,
    #         "low": self.all_low,
    #         "close": self.all_close,
    #         "volume": self.all_volume,
    #         "market_capital": self.all_market_capital,
    #     }
    #     return self.all_price_dict

    # def format_price_data(self, item):
    #     selected_data = self.raw_price_data[["date", item, "company_symbol"]]
    #     pivot_data = selected_data.pivot_table(
    #         index="date", columns="company_symbol", values=item
    #     )
    #     return pivot_data

    # # 處理stock finace report的functions
    # def format_report_data(self, factor):
    #     # 把factor的值取出來
    #     unique_ids = self.raw_report_data["factor_name"].unique()
    #     # 建立一個dict來存放個個factor
    #     dfs_by_id = {}
    #     # 根據唯一的factor建立DF
    #     for unique_id in unique_ids:
    #         temp_df = self.raw_report_data[
    #             self.raw_report_data["factor_name"] == unique_id
    #         ].pivot(index="date", columns="company_symbol", values="factor_value")
    #         dfs_by_id[unique_id] = temp_df

    #     # 印出每個factor的DF
    #     # for unique_id, temp_df in dfs_by_id.items():
    #     #     print(f"DataFrame for factor_name {unique_id}:\n{temp_df}\n")
    #     # 印出單一factor的DF
    #     print(f"DataFrame for factor_name {factor}:\n")
    #     # print(dfs_by_id[factor])
    #     return dfs_by_id[factor]


if __name__ == "__main__":
    data = Data()
    # 測試輸出股價資料
    # close = data.get("price:close")
    # print("收盤價:", close)
    # 測試輸出財報資料
    roe = data.get("report:roe, EPS")
