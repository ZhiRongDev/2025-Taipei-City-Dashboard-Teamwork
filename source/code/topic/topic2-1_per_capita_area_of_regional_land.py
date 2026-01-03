"""
df_asylum 為讀取 clean\合併\避難收容處所合併.csv 取 '名稱,縣市,鄉鎮,村里,類型,容納人數,收容所面積（平方公尺）,水災,震災,土石流,海嘯,救濟支站,無障礙設施,室內,室外' 這些欄位
1. 將 '水災,震災,土石流,海嘯,救濟支站,無障礙設施,室內,室外' 欄位中 將值做轉換{'是': 1, 'Y': 1, '備用':1, '否': 0, 'N': 0, '否(備援)': 0, '老舊聚落':0}，並將空值補0
2. 將 '縣市,鄉鎮' 欄位轉換為 'City,Town'

df_pol 為 讀取 clean\合併\merged_population.csv 取 '縣市名稱,鄉鎮市區名稱,人口數' 欄位
1. 將 '縣市名稱,鄉鎮市區名稱' 轉換為 'City,Town'
2. 以 (City,Town) 為組別計算各區域 df_pol 的人口數
3. 以 (City,Town) 為組別計算各區域 df_asylum 的收容所面積（平方公尺）除以 df_pol 的人口數，得到每人可分配的收容所面積（平方公尺），並將結果存入 df_asylum 新欄位

將 df_asylum 依照 'City' 分別輸出到 新北市(topic\newtaipeis\topic2-1__Town__asylum__pol_land_rate.csv) 與 臺北市(topic\taipei\topic2-1__Town__asylum__pol_land_rate.csv)
topic2-1__Town__pol_land_rate.csv

"""
import pandas as pd
import os

# 讀取避難收容處所資料
df_asylum = pd.read_csv(
    r'clean\合併\避難收容處所合併.csv',
    usecols=['名稱', '縣市', '鄉鎮', '村里', '類型', '容納人數', '收容所面積（平方公尺）',
             '水災', '震災', '土石流', '海嘯', '救濟支站', '無障礙設施', '室內', '室外']
)

# 需轉換的欄位
bool_cols = ['水災', '震災', '土石流', '海嘯', '救濟支站', '無障礙設施', '室內', '室外']
for col in bool_cols:
    df_asylum[col] = df_asylum[col].astype(str).str.strip().replace(
        {'是': 1, 'Y': 1, '備用': 1, '否': 0, 'N': 0, '否(備援)': 0, '老舊聚落': 0}
    ).replace('nan', 0).fillna(0).astype(int)

# 欄位名稱標準化
df_asylum = df_asylum.rename(columns={'縣市': 'City', '鄉鎮': 'Town'})

# 讀取人口資料
df_pol = pd.read_csv(
    r'clean\合併\merged_population.csv',
    usecols=['縣市名稱', '鄉鎮市區名稱', '人口數']
)
df_pol = df_pol.rename(columns={'縣市名稱': 'City', '鄉鎮市區名稱': 'Town'})
# 以 (City, Town) 為組別計算各區域人口數總和
df_pol = df_pol.groupby(['City', 'Town'], as_index=False)['人口數'].sum()


# 先將收容所面積、容納人數轉為 float
df_asylum['收容所面積（平方公尺）'] = pd.to_numeric(df_asylum['收容所面積（平方公尺）'], errors='coerce').fillna(0)
df_asylum['容納人數'] = pd.to_numeric(df_asylum['容納人數'], errors='coerce').fillna(0).round(0)

# 以 City, Town 分組，計算各 Town 的容納人數、收容所面積總和
df_asylum_grouped = df_asylum.groupby(['City', 'Town'], as_index=False).agg({
    '容納人數': 'sum',
    '收容所面積（平方公尺）': 'sum'
})

# 合併人口數
df_asylum_grouped = pd.merge(
    df_asylum_grouped,
    df_pol[['City', 'Town', '人口數']],
    on=['City', 'Town'],
    how='left'
)

# 移除無法轉換為 float 的人口數
df_asylum_grouped = df_asylum_grouped[
    pd.to_numeric(df_asylum_grouped['人口數'], errors='coerce').notnull()
]
df_asylum_grouped['人口數'] = df_asylum_grouped['人口數'].astype(float)

# 計算每人可分配的收容所面積
df_asylum_grouped['每人可分配收容所面積（平方公尺）'] = (
    df_asylum_grouped['收容所面積（平方公尺）'] / df_asylum_grouped['人口數']
)
df_asylum_grouped['每人可分配收容所面積（平方公尺）'] = df_asylum_grouped['每人可分配收容所面積（平方公尺）'].fillna(0)
df_asylum_grouped['每萬人可分配收容所面積（平方公尺）'] = df_asylum_grouped['每人可分配收容所面積（平方公尺）'] * 10000

# 移除 City 為空值的資料
df_asylum_grouped = df_asylum_grouped[df_asylum_grouped['City'].notnull() & (df_asylum_grouped['City'].astype(str).str.strip() != '')]

# 依照 City 輸出
output_info = [
    ('新北市', r'topic\newtaipeis\topic2-1__Town__asylum__pol_land_rate.csv'),
    ('臺北市', r'topic\taipei\topic2-1__Town__asylum__pol_land_rate.csv')
]

df_asylum_grouped['人口數'] = df_asylum_grouped['人口數'].astype(int)
df_asylum_grouped['容納人數'] = df_asylum_grouped['容納人數'].astype(int)
df_asylum_grouped['收容所面積（平方公尺）'] = df_asylum_grouped['收容所面積（平方公尺）'].astype(float).round(2)
df_asylum_grouped['每萬人可分配收容所面積（平方公尺）'] = df_asylum_grouped['每萬人可分配收容所面積（平方公尺）'].round(2)

for city, out_path in output_info:
    df_city = df_asylum_grouped[df_asylum_grouped['City'] == city]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df_city.to_csv(out_path, index=False, encoding='utf-8-sig')