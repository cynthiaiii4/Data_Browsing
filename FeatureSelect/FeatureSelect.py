import pandas as pd
from database import Database
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

def FeatureSelect(filtered_data):

    features_amount=5

    db=Database()
    column_type = db.get_column_type()
    category_columns = column_type[column_type['type'] == '類別']['column_zh'].tolist()

    # 使用 pd.get_dummies 進行 One-Hot Encoding
    filtered_data_noinf = filtered_data.replace([np.inf, -np.inf], np.nan).dropna()
    filtered_drop = filtered_data_noinf.dropna(subset=['區間股價變化'])
    features_fill = filtered_drop.fillna(0)
    y=features_fill['區間股價變化率']
    drop_col=['證券代碼','公司','區間股價變化','區間股價變化率','產業別','股價變化率分组']
    filtered_clean = features_fill.drop(drop_col, axis=1) 
    df_encoded = pd.DataFrame()
    for col in filtered_clean.columns:
        if col in category_columns:
            encoded_col = pd.get_dummies(filtered_clean[col], prefix=col)
            df_encoded = pd.concat([df_encoded, encoded_col], axis=1)
        else:
            df_encoded[col] = filtered_clean[col]

    # 計算每個特徵的得分
    scores, _ = f_regression(df_encoded, y)

    # 創建一個 DataFrame，包含特徵名稱和對應的得分
    feature_scores = pd.DataFrame({'Feature': df_encoded.columns, 'Score': scores})

    # 按得分降序排序
    feature_scores = feature_scores.sort_values(by='Score', ascending=False)

    selected_feature_names = feature_scores['Feature'].to_list()


    #依序取得排名前n的值
    selected_features_info = {}  
   
    for feature_name in selected_feature_names:
        parts = feature_name.split("_")
        if len(parts) > 0:
            result = parts[0]
        else:
            result = feature_name
        # 使用 feature_name 為key，找到對應的type
        feature_type = column_type.loc[column_type['column_zh'] == result, 'type'].values[0]
        selected_features_info[result] = feature_type
        # 如果已經找到所需特徵個數，退出迴圈
        if len(selected_features_info) == features_amount:
            break
    return selected_features_info