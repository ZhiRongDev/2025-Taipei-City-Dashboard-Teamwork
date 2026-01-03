import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
import os

# 讀取 town_coordinates_list.csv
df = pd.read_csv('merge/town_coordinates_list.csv')
df = df.dropna(subset=['Lat', 'Lon'])

# 讀取人口資料，只取需要的欄位
pop = pd.read_csv('clean/合併/merged_population.csv', usecols=['縣市名稱', '鄉鎮市區名稱', '戶數', '人口數', '資料時間'])
# 欄位名稱轉換
pop = pop.rename(columns={
    '縣市名稱': 'City',
    '鄉鎮市區名稱': 'Town',
    '戶數': 'households',
    '人口數': 'population',
    '資料時間': 'time'
})
# 選取 time 為 '113Y12M'
pop = pop[pop['time'] == '113Y12M']

'''
讀取 merge\town_coordinates_list.csv 檔案

針對每個 Source 建立四個 DataFrame
每個 df 計算各區域(City,Town)的總數
並針對經緯度資訊(Lat,Lon)計算各區域(City,Town)中點的疏離程度
'''
# 取得所有 Source
sources = df['Source'].unique()


def spatial_entropy(coords):
    """
    Calculates the spatial entropy of a set of coordinates using a simple grid-based method.

    Spatial entropy is a measure of the dispersion or randomness of points in space. 
    A higher entropy value indicates that the points are more evenly or randomly distributed, 
    while a lower value suggests clustering or concentration.

    Args:
        coords (np.ndarray): A 2D numpy array of shape (n_points, 2), where each row represents 
            the latitude and longitude of a point.

    Returns:
        float: The spatial entropy value. Returns 0 if fewer than 2 points are provided.

    Method:
        - The latitude and longitude ranges are divided into 10 bins each, forming a grid.
        - Each point is assigned to a grid cell based on its coordinates.
        - The number of points in each grid cell is counted.
        - The probability distribution of points across grid cells is computed.
        - Entropy is calculated using the formula: -sum(p * log(p)) for all grid cells with points.

    Note:
        This method provides a simple approximation of spatial entropy and may be sensitive to 
        the choice of grid size and the spatial extent of the data.
    """
    # 使用簡單的格網法計算空間熵
    if len(coords) < 2:
        return 0
    # 將經緯度離散化為格網
    lat_bins = np.linspace(coords[:,0].min(), coords[:,0].max(), 10)
    lon_bins = np.linspace(coords[:,1].min(), coords[:,1].max(), 10)
    digitized = np.vstack([
        np.digitize(coords[:,0], lat_bins),
        np.digitize(coords[:,1], lon_bins)
    ]).T
    # 統計每個格網的點數
    _, counts = np.unique([tuple(x) for x in digitized], axis=0, return_counts=True)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log(probs))
    return entropy

for source in sources:
    df_source = df[df['Source'] == source]

    # 計算各區域(City, Town)的總數
    count_df = df_source.groupby(['City', 'Town']).size().reset_index(name='Count')

    # 合併人口資料
    merged = pd.merge(count_df, pop, on=['City', 'Town'], how='left')

    # 計算比值
    merged['households_per_count'] = merged['households'] / merged['Count']
    merged['population_per_count'] = merged['population'] / merged['Count']

    # 計算各區域(City, Town)中點的疏離程度（平均兩兩距離）與空間熵
    def calc_dispersion_entropy(group):
        coords = group[['Lat', 'Lon']].values
        if len(coords) < 2:
            return pd.Series({'Dispersion': 0, 'SpatialEntropy': 0})
        dists = pdist(coords)
        dispersion = dists.mean()
        entropy = spatial_entropy(coords)
        return pd.Series({'Dispersion': dispersion, 'SpatialEntropy': entropy})

    dispersion_df = df_source.groupby(['City', 'Town']).apply(calc_dispersion_entropy).reset_index()

    # 合併結果
    result_df = pd.merge(merged, dispersion_df, on=['City', 'Town'])
    result_df[['households_per_count', 'population_per_count', 'Dispersion', 'SpatialEntropy']] = result_df[['households_per_count', 'population_per_count', 'Dispersion', 'SpatialEntropy']].fillna(0)

    # 輸出到 topic 資料夾下，以 source 命名
    # 依 City 分開輸出
    for city, folder in [('臺北市', 'taipei'), ('新北市', 'newtaipeis')]:
        city_df = result_df[result_df['City'] == city]
        if not city_df.empty:
            output_path = f'topic/{folder}/topic1-1__Town__regional_discrete_count({source}).csv'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            city_df.to_csv(output_path, index=False)
