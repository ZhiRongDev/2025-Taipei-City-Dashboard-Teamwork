import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
import os

# 讀取經緯度資料
df = pd.read_csv('merge/town_coordinates_list.csv')
df = df.dropna(subset=['Lat', 'Lon'])

# 讀取人口資料，只取需要的欄位
pop = pd.read_csv('clean/合併/merged_population.csv', usecols=['縣市名稱', '鄉鎮市區名稱', '戶數', '人口數', '資料時間'])
pop = pop.rename(columns={
    '縣市名稱': 'City',
    '鄉鎮市區名稱': 'Town',
    '戶數': 'households',
    '人口數': 'population',
    '資料時間': 'time'
})
pop = pop[pop['time'] == '113Y12M']

sources = df['Source'].unique()
dfs = {}

def spatial_entropy(coords):
    if len(coords) < 2:
        return 0
    lat_bins = np.linspace(coords[:,0].min(), coords[:,0].max(), 10)
    lon_bins = np.linspace(coords[:,1].min(), coords[:,1].max(), 10)
    digitized = np.vstack([
        np.digitize(coords[:,0], lat_bins),
        np.digitize(coords[:,1], lon_bins)
    ]).T
    _, counts = np.unique([tuple(x) for x in digitized], axis=0, return_counts=True)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log(probs))
    return entropy

for source in sources:
    df_source = df[df['Source'] == source]

    # 計算各 City 的總數
    count_df = df_source.groupby('City').size().reset_index(name='Count')

    # 對人口資料進行 City 級別的彙總
    pop_city = pop.groupby('City')[['households', 'population']].sum().reset_index()

    # 合併人口資料
    merged = pd.merge(count_df, pop_city, on='City', how='left')

    # 計算每筆資料的平均人口/戶數對應點數
    merged['households_per_count'] = merged['households'] / merged['Count']
    merged['population_per_count'] = merged['population'] / merged['Count']

    # 計算每個 City 中點的疏離程度與空間熵
    def calc_dispersion_entropy(group):
        coords = group[['Lat', 'Lon']].values
        if len(coords) < 2:
            return pd.Series({'Dispersion': 0, 'SpatialEntropy': 0})
        dists = pdist(coords)
        dispersion = dists.mean()
        entropy = spatial_entropy(coords)
        return pd.Series({'Dispersion': dispersion, 'SpatialEntropy': entropy})

    dispersion_df = df_source.groupby('City')[['Lat', 'Lon']].apply(calc_dispersion_entropy).reset_index()

    # 合併所有結果
    result_df = pd.merge(merged, dispersion_df, on='City', how='left')
    result_df[['households_per_count', 'population_per_count', 'Dispersion', 'SpatialEntropy']] = result_df[['households_per_count', 'population_per_count', 'Dispersion', 'SpatialEntropy']].fillna(0)

    dfs[source] = result_df

    # 依 City 分開輸出
    for city, folder in [('臺北市', 'taipei'), ('新北市', 'newtaipeis')]:
        city_df = result_df[result_df['City'] == city]
        if not city_df.empty:
            output_path = f'topic/{folder}/topic1-2__City__regional_discrete_count({source}).csv'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            city_df.to_csv(output_path, index=False)
