import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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
        # max_value= df['區間股價變化率'].max()
        # min_value = df['區間股價變化率'].min()
        max_value = np.clip(df['區間股價變化率'].max(), 10, 50)
        min_value = np.clip(df['區間股價變化率'].min(), -10, -50)
        df=df[df['區間股價變化率'].notnull() | df['區間股價變化率'].notna()]
        df['資本額(千萬)'] = (df['資本額']/10000000).round(2)

        fig = px.treemap(
            df, 
            path=['公司'],  # category型
            values='資本額(千萬)', 
            color='區間股價變化率', 
            hover_data=['證券代碼','公司', '資本額', '規模', '產業名稱', '區間股價變化', '區間股價變化率'],
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
        pie_data = pd.DataFrame({'產業名稱': category_counts.index, 'Counts': category_counts.values})

        # 計算同一產業下，區間股價變化率>0和<=0的數量
        positive_counts = []
        negative_counts = []

        for industry in pie_data['產業名稱']:
            positive_count = len(df[(df['產業名稱'] == industry) & (df['區間股價變化率'] > 0)])
            negative_count = len(df[(df['產業名稱'] == industry) & (df['區間股價變化率'] <= 0)])
            positive_counts.append(positive_count)
            negative_counts.append(negative_count)

        pie_data['上漲家數'] = positive_counts
        pie_data['下跌家數'] = negative_counts

        hovertext = []
        for _ ,row in pie_data.iterrows():
            hovertext.append(f"{row['產業名稱']}")
        # hover後的內容
        hoverinfo = []
        hovertemplate = []
        for _, row in pie_data.iterrows():
            hoverinfo.append(f"{row['產業名稱']}<br>Counts: {row['Counts']}<br>上漲家數: {row['上漲家數']}<br>下跌家數: {row['下跌家數']}")
            hovertemplate.append(f"{row['產業名稱']}<br>Counts: {row['Counts']}<br>上漲家數: {row['上漲家數']}<br>下跌家數: {row['下跌家數']}")

        fig = go.Figure(data=[go.Pie(
            labels=pie_data['產業名稱'],
            values=pie_data['Counts'],
            hoverinfo='text+percent',
            text=hovertext,
            hovertemplate=hovertemplate,
            name=''
        )])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.show()
        fig.write_html('graph/1/my_pie_plot.html')
        

    '''
    建立靜態和動態長條圖。靜態用來顯示在pdf，動態用來顯示在html
    '''
    def get_bar_chart_all(self):
        df=self.filtered_data
        #靜態
        # 計算股價變化率的最小值和最大值
        min_value = df['區間股價變化率'].min()
        max_value = df['區間股價變化率'].max()

        # 計算分組區間，以間隔2在最大值和最小值間分群
        step = 2
        bins = list(range(int(min_value) - step, int(max_value) + 2 * step, step))

        # 將股價變化率分群
        df['股價變化率分组'] = pd.cut(df['區間股價變化率'], bins=bins)

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
            xaxis_title="股價變化率",
            yaxis_title="數量",
            title="個股漲跌概況",
            xaxis={'categoryorder': 'total ascending'},
            xaxis_categoryorder='category ascending'
        )

        # 設置x軸類別順序
        x_order = grouped_data['股價變化率分组'].tolist()
        fig.update_xaxes(categoryorder='array', categoryarray=x_order)

        fig.show()
        fig.write_html('graph/1/my_bar_plot.html')

        