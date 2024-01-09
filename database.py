import configparser
from Utils.config import Config
import pymysql
import pandas as pd
import os


class Database:
    def __init__(self):
        self._config = Config()
        self._db_data = self._config.get_database_config()
        self.column_mapping = self.get_column_info()
        # self.connection()

    # 建立與DB的連線
    def create_connection(self):
        # 檢查DB版本&連線成功
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            config_host = config["database"]["host"]
            config_port = int(config["database"]["port"])
            config_user = config["database"]["user"]
            config_password = config["database"]["password"]
            config_db = config["database"]["db"]
            config_charset = config["database"]["charset"]

            db = pymysql.connect(
                host=config_host,
                port=config_port,
                user=config_user,
                passwd=config_password,
                db=config_db,
                charset=config_charset,
            )
            return db
        except Exception as e:
            print(e)
            print("無法連結資料庫")
            return e

    # 取得公司價量資訊(stock)
    def get_stock(self,start_d,end_d):
        DATA_DIR = 'data'
        file_names = ['stock24_1.csv', 'stock24_2.csv', 'stock24_3.csv', 'stock24_4.csv', 'stock24_5.csv', 'stock24_6.csv', 'stock24_7.csv', 'stock24_8.csv', 'stock24_9.csv', 'stock24_10.csv', 'stock24_11.csv', 'stock24_12.csv']
        combined_df_from_db = pd.DataFrame()
        for file_name in file_names:
            data_path = os.path.join(DATA_DIR, file_name)
            df_from_db = pd.read_csv(data_path)
            combined_df_from_db = pd.concat([combined_df_from_db, df_from_db], ignore_index=True)
        combined_df_from_db['date'] = pd.to_datetime(combined_df_from_db['date'])
        filtered_df_from_db = combined_df_from_db[(combined_df_from_db['date'] >= start_d) & (combined_df_from_db['date'] <= end_d)]
        filtered_df_from_db = filtered_df_from_db.copy()
        # DATA_DIR = 'data'
        # FILE_NAME1 = 'stock102507.csv'
        # data_path1 = os.path.join(DATA_DIR, FILE_NAME1)
        # df_from_db1 = pd.read_csv(data_path1)
        # df_from_db=df_from_db1

        # df_from_db['date'] = pd.to_datetime(df_from_db['date'])
        # filtered_df_from_db = df_from_db[(df_from_db['date'] >= start_d) & (df_from_db['date'] <= end_d)]
        filtered_df_from_db.rename(columns=self.column_mapping, inplace=True)
        return filtered_df_from_db
    # def get_stock(self,start_d,end_d):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()

    #             # 使用参数化查询
    #             sql = "SELECT * FROM ccthesis.stock WHERE date BETWEEN %s AND %s"

    #             # 执行查询
    #             cursor.execute(sql, (start_d, end_d))
    #             data = cursor.fetchall()
    #             columns = [
    #                 "id",
    #                 "company_id",
    #                 "date",
    #                 "open",
    #                 "high",
    #                 "low",
    #                 "close",
    #                 "volume",
    #                 "ma5",
    #                 "ma10",
    #                 "ma20",
    #                 "ma60",
    #                 "mavol_5",
    #                 "mavol_10",
    #                 "mavol_20",
    #                 "mavol_60",
    #             ]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             df_from_db.rename(columns=self.column_mapping, inplace=True)
    #             return df_from_db

    #     except Exception as e:
    #         print(e)
    #         print("get_stock無法執行SQL語法")
    #         return e
        
    # 取得指數價量資訊(market_index)
    def get_market_index(self,start_d,end_d):
        DATA_DIR = 'data'
        file_names = ['market1025.csv', 'market24.csv']
        combined_df_from_db = pd.DataFrame()
        for file_name in file_names:
            data_path = os.path.join(DATA_DIR, file_name)
            df_from_db = pd.read_csv(data_path)
            combined_df_from_db = pd.concat([combined_df_from_db, df_from_db], ignore_index=True)
        combined_df_from_db['date'] = pd.to_datetime(combined_df_from_db['date'])
        filtered_df_from_db = combined_df_from_db[(combined_df_from_db['date'] >= start_d) & (combined_df_from_db['date'] <= end_d)]
        filtered_df_from_db = filtered_df_from_db.copy()
        # DATA_DIR = ''
        # FILE_NAME = 'data/market1025.csv'
        # data_path = os.path.join(DATA_DIR, FILE_NAME)
        # df_from_db = pd.read_csv(data_path)
        # df_from_db['date'] = pd.to_datetime(df_from_db['date'])
        # filtered_df_from_db = df_from_db[(df_from_db['date'] >= start_d) & (df_from_db['date'] <= end_d)]
        filtered_df_from_db.rename(columns=self.column_mapping, inplace=True)
        return filtered_df_from_db
    # def get_market_index(self,start_d,end_d):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()

    #             # 使用参数化查询
    #             sql = "SELECT * FROM ccthesis.market_index WHERE date BETWEEN %s AND %s"

    #             # 执行查询
    #             cursor.execute(sql, (start_d, end_d))
    #             data = cursor.fetchall()
    #             columns = [
    #                 "id",
    #                 "index_name",
    #                 "date",
    #                 "open",
    #                 "high",
    #                 "low",
    #                 "close",
    #                 "volume",
    #                 "ma5",
    #                 "ma10",
    #                 "ma20",
    #                 "ma60",
    #                 "mavol_5",
    #                 "mavol_10",
    #                 "mavol_20",
    #                 "mavol_60",
    #             ]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             df_from_db.rename(columns=self.column_mapping, inplace=True)
    #             return df_from_db

    #     except Exception as e:
    #         print(e)
    #         print("get_market_index無法執行SQL語法")
    #         return e

    # 取得公司資料(company)
    def get_company_basic(self):
        DATA_DIR = ''
        FILE_NAME = 'data/company_basic1025.csv'
        data_path = os.path.join(DATA_DIR, FILE_NAME)
        df_from_db = pd.read_csv(data_path)
        #TODO:規模何時算?
        df_from_db = df_from_db.sort_values(by='capital', ascending=False)
        df_from_db['scale'] = '小'
        df_from_db.loc[df_from_db.sort_values(by='capital', ascending=False).index[:50], 'scale'] = '大'
        df_from_db.loc[df_from_db.sort_values(by='capital', ascending=False).index[50:150], 'scale'] = '中'
        df_from_db.rename(columns=self.column_mapping, inplace=True)
        return df_from_db
    # def get_company_basic(self):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()
    #             sql = " SELECT * FROM ccthesis.company"
    #             cursor.execute(sql)
                
    #             data = cursor.fetchall()
    #             columns = ["id","company_id", "company_name", "market", "industry", "industry_name", "capital"]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             df_from_db.rename(columns=self.column_mapping, inplace=True)
    #             return df_from_db

    #     except Exception as e:
    #         print(e)
    #         print("get_company_basic無法執行SQL語法")
    #         return e
        
        # 取得籌碼資料(chips)
    def get_chips(self,start_d,end_d):
        DATA_DIR = 'data'
        file_names = ['combine_chips.csv']
        combined_df_from_db = pd.DataFrame()
        for file_name in file_names:
            data_path = os.path.join(DATA_DIR, file_name)
            df_from_db = pd.read_csv(data_path)
            combined_df_from_db = pd.concat([combined_df_from_db, df_from_db], ignore_index=True)
        combined_df_from_db['date'] = pd.to_datetime(combined_df_from_db['date'])
        filtered_df_from_db = combined_df_from_db[(combined_df_from_db['date'] >= start_d) & (combined_df_from_db['date'] <= end_d)]
        filtered_df_from_db = filtered_df_from_db.copy()
        filtered_df_from_db.rename(columns=self.column_mapping, inplace=True)
        return filtered_df_from_db
    # def get_chips(self,start_d,end_d):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()
    #             sql = "SELECT * FROM ccthesis.chips WHERE date BETWEEN %s AND %s"

    #             # 执行查询
    #             cursor.execute(sql, (start_d, end_d))
    #             data = cursor.fetchall()
    #             columns = [
    #                 "id",
    #                 "date",
    #                 "company_id", 
    #                 "foreign_investors", 
    #                 "investment_banks", 
    #                 "dealer", 
    #                 "all_institutional_investors", 
    #                 "foreign_investors_day",
    #                 "investment_banks_days",
    #                 "dealer_days",
    #                 "all_institutional_investors_days",
    #                 "directors_stock_ratio",
    #                 "directors_stock",
    #                 "financing_balance",
    #                 "margin_balance",
    #                 "sale_margin_purchase_ratio",
    #                 "margin_balance_ratio",
    #                 "financing_balance_ratio",
    #                 "200_400_ratio",
    #                 "400_600_ratio",
    #                 "600_800_ratio",
    #                 "800_1000_ratio",
    #                 "1000up_ratio"
    #                 ]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             df_from_db.rename(columns=self.column_mapping, inplace=True)
    #             return df_from_db
			 																		

    #     except Exception as e:
    #         print(e)
    #         print("get_chips無法執行SQL語法")
    #         return e
        
    # 取得月報資料(finance_report_m)
    def get_finance_report_m(self):
        DATA_DIR = 'data'
        file_names = ['finalreport_m1025.csv','finalreport_m1231.csv']
        combined_df_from_db = pd.DataFrame()
        for file_name in file_names:
            data_path = os.path.join(DATA_DIR, file_name)
            df_from_db = pd.read_csv(data_path)
            combined_df_from_db = pd.concat([combined_df_from_db, df_from_db], ignore_index=True)
        combined_df_from_db['m_date'] = pd.to_datetime(combined_df_from_db['m_date'])
        df_from_db=combined_df_from_db
        # DATA_DIR = ''
        # FILE_NAME = 'data/finalreport_m1025.csv'
        # data_path = os.path.join(DATA_DIR, FILE_NAME)
        # df_from_db = pd.read_csv(data_path)
        df_from_db.rename(columns=self.column_mapping, inplace=True)
        return df_from_db
    # def get_finance_report_m(self):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()
    #             sql = f" SELECT * FROM ccthesis.finance_report_m"

    #             cursor.execute(sql)
    #             data = cursor.fetchall()
    #             columns = [
    #                 "id",
    #                 "date",
    #                 "company_id", 
    #                 "revenue_release_date", 
    #                 "revenue_m", 
    #                 "revenue_m_lastyear", 
    #                 "revenue_vs_lastyear_ratio", 
    #                 "revenue_mom_ratio",
    #                 "revenue_growth_month",
    #                 "cumulative_revenue",
    #                 "cumulative_revenue_lastyear",
    #                 "cumulative_revenue_vs_lastyear_ratio"
    #                 ]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             df_from_db.rename(columns=self.column_mapping, inplace=True)
    #             return df_from_db
			 																		

    #     except Exception as e:
    #         print(e)
    #         print("get_finance_report_m無法執行SQL語法")
    #         return e
        
    # 取得季報資料(finance_report_q)
    def get_finance_report_q(self):
        DATA_DIR = 'data'
        file_names = ['finalreport_Q10253.csv','finalreport_Q24.csv']
        combined_df_from_db = pd.DataFrame()
        for file_name in file_names:
            data_path = os.path.join(DATA_DIR, file_name)
            df_from_db = pd.read_csv(data_path)
            combined_df_from_db = pd.concat([combined_df_from_db, df_from_db], ignore_index=True)
        combined_df_from_db['q_date'] = pd.to_datetime(combined_df_from_db['q_date'])
        df_from_db=combined_df_from_db
        # DATA_DIR = ''
        # FILE_NAME = 'data/finalreport_Q10253.csv'
        # data_path = os.path.join(DATA_DIR, FILE_NAME)
        # df_from_db = pd.read_csv(data_path)
        df_from_db.rename(columns=self.column_mapping, inplace=True)
        return df_from_db
    # def get_finance_report_q(self):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()
    #             sql = f" SELECT * FROM ccthesis.finance_report_q"

    #             cursor.execute(sql)
    #             data = cursor.fetchall()
    #             columns = [
    #                 "id",
    #                 "date",
    #                 "company_id", 
    #                 "Q", 
    #                 "q_report_issued", 
    #                 "EPS", 
    #                 "PB", 
    #                 "PSR",
    #                 "PE",
    #                 "ROA_C",
    #                 "ROA_A",
    #                 "ROA_B",
    #                 "ROE_A",
    #                 "ROE_B",
    #                 "operating_profit_margin",
    #                 "operating_profit_growth_rate",
    #                 " operating_profit_variability_rate",
    #                 "operating_profit_to_paid-up_capital_ratio",
    #                 "net_income_margin",
    #                 "net_profit_variability_rate_Q",
    #                 "ebitda_margin",
    #                 "earnings_before_tax_margin",
    #                 "earnings_before_tax_growth_rate",
    #                 "net_profit_margin",
    #                 "net_profit_growth_rate",
    #                 "stock_market_value_EOQ",
    #                 "revenue_growth_rate",
    #                 "revenue_variability_rate",
    #                 "equity_to_assets_ratio",
    #                 "total_asset_growth_rate",
    #                 "total_asset_turnover_ratio",
    #                 "NOIR",
    #                 "gross_profit_rate",
    #                 "gross_profit_growth_rate",
    #                 "realized_sales_gross_profit_growth_rate",
    #                 "realized_sales_gross_profit_margin",
    #                 "free_cash_flow",
    #                 "net_operating_revenue",
    #                 "shareholders_equity",
    #                 "cash_flow_from_operations"
    #                 ]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             df_from_db.rename(columns=self.column_mapping, inplace=True)
    #             return df_from_db
			 																		

    #     except Exception as e:
    #         print(e)
    #         print("get_finance_report_q無法執行SQL語法")
    #         return e
    # 取得欄位資料(column_info)
    def get_column_info(self):
        DATA_DIR = ''
        FILE_NAME = 'data/column_info1.csv'
        data_path = os.path.join(DATA_DIR, FILE_NAME)
        df_from_db = pd.read_csv(data_path)
        column_mapping = dict(zip(df_from_db['column'], df_from_db['column_zh']))
        return column_mapping
    def get_column_type(self):
        DATA_DIR = ''
        FILE_NAME = 'data/column_info1.csv'
        data_path = os.path.join(DATA_DIR, FILE_NAME)
        df_from_db = pd.read_csv(data_path)
        return df_from_db
    # def get_column_info(self):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()
    #             sql = f" SELECT * FROM ccthesis.column_info"

    #             cursor.execute(sql)
    #             data = cursor.fetchall()
    #             columns = [
    #                 "id",
    #                 "column",
    #                 "column_zh", 
    #                 "type"
    #                 ]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             column_mapping = dict(zip(df_from_db['column'], df_from_db['column_zh']))
    #             return column_mapping
			 																		

    #     except Exception as e:
    #         print(e)
    #         print("get_column_info無法執行SQL語法")
    #         return e
        
    # def get_column_info(self):
    #     try:
    #         with self.create_connection() as db:
    #             cursor = db.cursor()
    #             sql = f" SELECT * FROM ccthesis.column_info"

    #             cursor.execute(sql)
    #             data = cursor.fetchall()
    #             columns = [
    #                 "id",
    #                 "column",
    #                 "column_zh", 
    #                 "type"
    #                 ]
    #             df_from_db = pd.DataFrame(data, columns=columns)
    #             return df_from_db
                                                                                    

    #     except Exception as e:
    #         print(e)
    #         print("get_column_info無法執行SQL語法")
    #         return e

# if __name__ == "__main__":
#     db = Database()
#     db.get_finance_report()

    # db.select_index('open')
