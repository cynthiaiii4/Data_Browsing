import pandas as pd
import xml.etree.ElementTree as ET

# role:哪個法人
# days:天數
def Chips(ch_data,*xml):
    
    #解析XML
    tree = ET.parse(xml[0])
    root = tree.getroot()
    role = root.find('role').text
    days = int(root.find('days').text)


    ch_data = ch_data.sort_values(by=["證券代碼", "日期"], ascending=[True, False])

    # 取第1筆資料
    last_1_records = ch_data.groupby('證券代碼').head(1)

    #判斷天數*-
    if days>=0:
        selected_companies = last_1_records.groupby('證券代碼').filter(lambda x: (x[role] >= days).all())['證券代碼'].unique()
    else:
        selected_companies = last_1_records.groupby('證券代碼').filter(lambda x: (x[role] <= days).all())['證券代碼'].unique()

    return selected_companies