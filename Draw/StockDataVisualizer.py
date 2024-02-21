import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import math

class StockDataVisualizer:
    def __init__(self, filtered_data):
        self.filtered_data = filtered_data
        # 設置中文字體
        sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})

    '''
    建立動態熱力圖
    '''
    def get_heat_map_all(self):
        df=self.filtered_data
        df['區間最大股價變化率'].fillna(0, inplace=True)
        # 將無窮大值（inf）替換為除了inf外的最大值
        max_value_without_inf = df['區間最大股價變化率'].replace([np.inf, -np.inf], np.nan).max(skipna=True)
        df['區間最大股價變化率'].replace([np.inf, -np.inf], max_value_without_inf, inplace=True)

        max_value = np.clip(df['區間最大股價變化率'].max(), 10, 50)
        min_value = np.clip(df['區間最大股價變化率'].min(), -10, -50)
        df=df[df['區間最大股價變化率'].notnull() | df['區間最大股價變化率'].notna()]
        df['資本額(千萬)'] = (df['資本額']/10000000).round(2)

        fig = px.treemap(
            df, 
            path=['產業名稱','公司'],  # category型
            values='資本額(千萬)', 
            color='區間最大股價變化率', 
            hover_data=['證券代碼','公司', '資本額', '規模', '產業名稱', '區間最大股價變化率', '區間最大股價變化率'],
            range_color=[min_value,max_value],
            # range_color=[-50, 50],
            color_continuous_scale='RdYlGn_r', 
            color_continuous_midpoint=0 , 
        )
        fig.update_traces(textinfo='label+value',textfont = dict(size = 10)) 
        fig.write_html('graph/1/my_plot.html')
        fig.show()
        

    '''
    建立靜態和動態圓餅圖。靜態用來顯示在pdf，動態用來顯示在html
    '''
    def get_industry_pie_all(self):
        df=self.filtered_data
        # 計算類別數量
        category_counts = df['產業名稱'].value_counts()

        # 靜態圖
        # 獲取類別標籤和計數
        labels = category_counts.index
        sizes = category_counts.values
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('類股支數占比')
        plt.axis('equal')  # 使圖形成圓形
        plt.savefig('graph/1/my_pie_plot.png')
        plt.show()

        # 動態圖
        # 建立數據df
        pie_data = pd.DataFrame({'證券代碼': df['證券代碼'], '產業名稱':df['產業名稱'],'區間最大股價變化率':df['區間最大股價變化率'] })
        # 定義自定義函數判斷上漲或下跌
        def label_trend(row):
            return '上漲' if row['區間最大股價變化率'] >= 0 else '下跌'
        pie_data['漲跌'] = pie_data.apply(label_trend, axis=1)
        pie_data['Counts']=1

        #繪圖
        fig = px.sunburst(pie_data, path=['產業名稱', '漲跌'], values='Counts', custom_data=['Counts'])
        #調整顯示和hover內容
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_traces(textinfo='label+value+percent parent')
        hover_template = f'<b>%{{label}}</b><br>Counts: %{{customdata[0]}}<br>佔比: %{{percentParent:.0%}}'
        fig.update_traces(hovertemplate=hover_template)
        fig.show()
        fig.write_html('graph/1/my_pie_plot.html')
        

    '''
    建立靜態和動態長條圖。靜態用來顯示在pdf，動態用來顯示在html
    '''
    def get_bar_chart_all(self):
        df=self.filtered_data

        # 將 NaN 替換為 0
        df['區間最大股價變化率'].replace({np.nan: 0}, inplace=True)

        # 將無窮大和無窮小值替換為 0
        df['區間最大股價變化率'].replace({np.inf: 0, -np.inf: 0}, inplace=True)
        #靜態
        # 計算股價變化率的最小值和最大值
        min_value = df['區間最大股價變化率'].min()
        max_value = df['區間最大股價變化率'].max()

        # 計算分組區間，以間隔2在最大值和最小值間分群
        step = 2
        bins = list(range(int(min_value) - step, int(max_value) + 2 * step, step))

        # 將股價變化率分群
        df['股價變化率分组'] = pd.cut(df['區間最大股價變化率'], bins=bins)

        # 計算分組內的公司數量
        grouped_data = self.filtered_data.groupby('股價變化率分组')['公司'].count()

        plt.bar(grouped_data.index.astype(str), grouped_data)

        #旋轉45度(字才不會重疊)
        plt.xticks(rotation=90)

        plt.title("個股漲跌概況")
        plt.xlabel("股價變化率")
        plt.ylabel("數量")
        plt.savefig('graph/1/my_bar_plot.png')
        plt.show()

        #動態
        # 計算分組公司數量並resetindex
        grouped_data = self.filtered_data.groupby('股價變化率分组')['公司'].count().reset_index()
        grouped_data['股價變化率分组'] = grouped_data['股價變化率分组'].astype(str)

        fig = px.bar(grouped_data, x='股價變化率分组', y='公司', labels={'股價變化率分组': '股價變化率'})

        fig.update_layout(
            xaxis_title="區間最大股價變化率",
            yaxis_title="數量",
            title="個股區間最大股價變化率漲跌概況",
            xaxis={'categoryorder': 'total ascending'},
            xaxis_categoryorder='category ascending'
        )

        # 設置x軸類別順序
        x_order = grouped_data['股價變化率分组'].tolist()
        fig.update_xaxes(categoryorder='array', categoryarray=x_order)

        fig.show()
        fig.write_html('graph/1/my_bar_plot.html')

        