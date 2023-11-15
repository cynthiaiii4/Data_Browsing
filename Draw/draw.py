import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.ticker as ticker
from itertools import combinations
import time

def Draw(data,features,*xml):
    # 建一个PDF文件
    #TODO:檔名加日期時間
    pdf_filename = 'output_plots.pdf'
    pdf_pages = PdfPages(pdf_filename)

    # 绘制其他图表并重复上述过程
    # 設置中文字體
    sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})
    if not xml:
        xml_f ="xml/stock_analysis.xml"
    else:
        xml_f= xml[0]
    #解析XML
    tree1 = ET.parse(xml_f)
    root1 = tree1.getroot()
    root1.findall('Graph')

    graph_dict = {}
    seq = 0

    # 取得Graphs
    start_time = time.time()
    for graph in root1.findall('Graph'):
        chart_type_element = graph.find('ChartType')
        chart_parm_element = graph.find('Chart_parm')

        # 取得X值，不固定數量
        X_values = [element.text for element in graph.findall('X')]

        f_Y_element = graph.find('Y')
        f_Y = f_Y_element.text if f_Y_element is not None else ''

        chart_type = chart_type_element.text if chart_type_element is not None else ''
        chart_parm = chart_parm_element.text if chart_parm_element is not None else ''

        graph_info = {'X': X_values, 'Y': f_Y, 'ChartType': chart_type, 'Chart_parm': chart_parm}
        graph_dict[seq] = graph_info
        seq += 1


    #畫出每個圖
    #TODO:類別化
    for key, values in graph_dict.items():
        y = values['Y']
        chart_type = values['ChartType']
        chart_parm = values['Chart_parm']

        # # 設置中文字體
        # sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})
        if chart_type == 'scatter':

            # 使用 Seaborn 繪製散點圖
            fig = plt.figure()
            sns.scatterplot(data=data, x=values['X'][0], y=y)
            plt.title(f'Scatter Plot of {values["X"][0]} vs {y}')
            plt.savefig('graph/scatter.png')
            pdf_start_time = time.time()
            pdf_pages.savefig(fig)
            plt.close()
        elif chart_type == 'catplot':

            fig = plt.figure()
            sns.catplot(x=values['X'][0], y=y, data=data, kind= chart_parm )  
            plt.title(f'Catplot of {values["X"][0]} vs {y}')
            plt.savefig('graph/catplot.png')
            pdf_pages.savefig(fig)
            plt.close()

        elif chart_type == 'pairplot':

            fig = plt.figure()
            sns.pairplot(data, vars=values['X'])
            plt.savefig('graph/pairplot.png')
            pdf_pages.savefig(fig)
            plt.close()

        elif chart_type == 'countplot':

            fig = plt.figure()
            ax = sns.countplot(x=values['X'][0], data=data) 
            plt.savefig('graph/countplot.png')
            pdf_pages.savefig(fig)
            plt.close()

        elif chart_type == 'displot':

            fig = plt.figure()
            sns.displot(data=data[values['X'][0]], kde=True, bins=20)
            plt.savefig('graph/displot.png') 
            pdf_pages.savefig(fig)
            plt.close()
        elif chart_type == 'regplot':

            fig = plt.figure()
            ax = sns.regplot(x=values['X'][0], y=y, data=data)
            plt.savefig('graph/regplot.png') 
            pdf_pages.savefig(fig)
            plt.close()
        elif chart_type == 'violinplot':

            fig = plt.figure()
            sns.violinplot(x=data[values['X'][0]], y=data[y])
            x_axis = plt.gca().xaxis
            x_axis.set_tick_params(rotation=45)
            plt.savefig('graph/violinplot.png') 
            pdf_pages.savefig(fig)
            plt.close()
        elif chart_type == 'bubbleplot':

            fig = plt.figure()
            sns.scatterplot(data=data, x=values['X'][0], y=y, size=values['X'][1], legend=False, sizes=(20, 2000))
            plt.savefig('graph/bubbleplot.png') 
            pdf_pages.savefig(fig)
            plt.close()
        plt.close()


   
        
    # 創建一個 FacetGrid，但不指定 col 和 row 參數
    p = sns.FacetGrid(data, hue='證券代碼')

    # 使用combinations生成所有不重複的3個欄位名稱的組合
    combinations_list = list(combinations(features, 3))
    
    # print('combinations_list')
    # print(combinations_list)
    # 遍歷所有欄位名稱的組合
    facetGrid =1
    for combo in combinations_list:

        col_name, row_name, scatter_col = combo
        # 動態生成新的欄位名稱，將原名稱後面添加 '_b'
        col_name_b = col_name + '_b'
        row_name_b = row_name + '_b'
        # 動態設定 col 和 row 參數
        
        data[col_name_b] = pd.qcut(data[col_name], q=5, duplicates='drop')
        data[row_name_b] = pd.qcut(data[row_name], q=5, duplicates='drop')
        
        p = sns.FacetGrid(data, col=col_name_b, row=row_name_b, hue='證券代碼', margin_titles=True)
            # 自定義繪圖函數
        def custom_scatter(*args, **kwargs):
            ax = plt.gca()  # 獲取當前子圖的座標軸對象
            ax.spines['bottom'].set_linewidth(3) # 設定底部線條寬度
            ax.spines['left'].set_linewidth(3)   # 設定左側線條寬度
            # 設定底部線條和左側線條的顏色為深黑色
            ax.spines['bottom'].set_color('black')
            ax.spines['left'].set_color('black')

            # 設定 Y 軸刻度標籤格式，以包含負號
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%+.2f"))
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%+.2f"))
            # 繪製散點圖或其他繪圖
            plt.scatter(*args, **kwargs)

        # 調整標題與圖的距離
        plt.subplots_adjust(top=0.7)  # 調整標題與圖的距離，可以根據需要調整top值
        #設定標題
        p.fig.suptitle(f"在不同{col_name}(X) 和 {row_name}(Y)區間中，{scatter_col}(x)和股價變化率(y)的表現", fontsize=16)
        p.map(custom_scatter, scatter_col, '區間股價變化率')

        for ax in p.axes.flat:
            ax.spines['bottom'].set_linewidth(3)
            ax.spines['left'].set_linewidth(3)
            ax.spines['bottom'].set_color('black')
            ax.spines['left'].set_color('black')
        pdf_pages.savefig(p.fig)
        p.fig.savefig(f'graph/facetGrid_{facetGrid}.png') 
        plt.show()
        plt.close()
        
        facetGrid+=1

    # 顯示圖形
    # plt.show()

    # 关闭PDF文件
    pdf_pages.close()

    print(f"所有图表已保存到 {pdf_filename}")