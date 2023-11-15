import pandas as pd
from database import Database
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

def FeatureSelect(filtered_data):
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
    
    # with pd.ExcelWriter('onehot.xlsx', engine='openpyxl') as writer:
    #     df_encoded.to_excel(writer, index=False, sheet_name='Sheet1')
    # 選擇要保留的特徵數

    select_k = 5

    # 使用填補後的特徵進行特徵選擇
    selection = SelectKBest(f_regression, k=select_k).fit(df_encoded, y)

    # 顯示保留的欄位
    selected_feature_names = df_encoded.columns[selection.get_support()]

    selected_features_info = {}  # 创建空字典

    # 遍历选定的特征名
    for feature_name in selected_feature_names:
        print(feature_name)
        parts = feature_name.split("_")
        if len(parts) > 0:
            result = parts[0]
        else:
            result = feature_name
        # 使用 feature_name 作为键，查找对应的 type 值，并存入字典
        feature_type = column_type.loc[column_type['column_zh'] == result, 'type'].values[0]
        selected_features_info[result] = feature_type

    return selected_features_info