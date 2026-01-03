"""
clean\合併\spot_list_經緯度.csv 為 df_spot，merge\town_coordinates_list.csv 為 df_item
透過 df_spot 與 df_item 經緯度計算 df_item['Source'] 中各項目(AED、警消、防空疏散地點、避難收容所)在 1, 5, 10公里內的數量
"""
import os
import pandas as pd
import numpy as np
from tqdm import tqdm

def haversine_vectorized(lat1, lon1, lat2, lon2):
    """
    向量化版本的 haversine 距離計算
    """
    R = 6371  # 地球半徑(公里)
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    
    return R * c

# 讀取CSV檔案
df_spot = pd.read_csv(r'clean\合併\spot_list_經緯度.csv')
df_spot = df_spot.rename(columns={'細分': '旅遊景點'})

df_item = pd.read_csv(r'merge\town_coordinates_list.csv')

# 初始化結果欄位
sources = ['AED', '警消', '防空疏散地點', '避難收容所']
distances = [1, 5, 10]  # 不同距離範圍

# 為每個來源和距離建立計數欄位
for source in sources:
    for dist in distances:
        df_spot[f'{source}_{dist}km'] = 0

# 使用向量化操作計算距離
for source in tqdm(sources, desc="Processing sources"):
    # 篩選特定類型的設施
    items = df_item[df_item['Source'] == source]
    
    # 創建網格點，計算所有點對之間的距離
    lat1 = df_spot['lat'].values[:, np.newaxis]
    lon1 = df_spot['lon'].values[:, np.newaxis]
    lat2 = items['Lat'].values
    lon2 = items['Lon'].values
    
    # 計算距離矩陣
    distances_matrix = haversine_vectorized(lat1, lon1, lat2, lon2)
    
    # 計算每個距離範圍內的設施數量
    for dist in distances:
        df_spot[f'{source}_{dist}km'] = (distances_matrix <= dist).sum(axis=1)

# 建立資料夾
os.makedirs(f'topic/taipei', exist_ok=True)
os.makedirs(f'topic/newtaipeis', exist_ok=True)

# 針對每個距離範圍輸出檔案
for dist in distances:
    # 準備該距離範圍的欄位
    result_columns = ['旅遊景點', 'lat', 'lon'] + [f'{source}_{dist}km' for source in sources]
    
    # 分別儲存臺北市和新北市的資料
    df_taipei = df_spot[df_spot['縣市'] == '臺北市'][result_columns]
    df_newtaipei = df_spot[df_spot['縣市'] == '新北市'][result_columns]
    
    # 輸出檔案
    df_taipei.to_csv(
        f'topic/taipei/topic_3-1_spot_source_count_in__{dist}km.csv', 
        index=False, 
        encoding='utf-8-sig'
    )
    df_newtaipei.to_csv(
        f'topic/newtaipeis/topic_3-1_spot_source_count__{dist}km.csv', 
        index=False, 
        encoding='utf-8-sig'
    )