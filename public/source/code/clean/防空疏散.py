import pandas as pd

# 讀取台北市資料
df_taipei = pd.read_csv(r'raw\防空疏散\114年臺北市防空疏散避難設施資料集Q1_1140501.csv')

# 只保留指定欄位
keep_cols = ['建築物名稱', '電腦編號', '村里別', '地址', '緯經度', '地下樓層數', '可容納人數', '轄管分局']
df_taipei = df_taipei[keep_cols]

# 欄位名稱轉換
df_taipei.columns = ['category', 'number', 'village', 'address', 'location', 'floor', 'capacity', 'unit']

# 讀取新北市資料
df_newtaipei = pd.read_csv(r'raw\防空疏散\新北市防空疏散避難設施數量及容量.csv')

# 刪除 note 欄位（如果存在）
if 'note' in df_newtaipei.columns:
    df_newtaipei = df_newtaipei.drop(columns=['note'])

# 假設新北市資料欄位順序與台北市相同，若不同請對應調整
df_newtaipei.columns = ['category', 'number', 'village', 'address', 'location', 'floor', 'capacity', 'unit']

# 合併兩份資料
df_all = pd.concat([df_taipei, df_newtaipei], ignore_index=True)

# location 欄位經緯度拆分
# 假設格式為 "lat,lon"
df_all[['lat', 'lon']] = df_all['location'].str.split(',', expand=True)
# df_all['lat'] = df_all['lat'].astype(float)

# 從 address 欄位用 regex 抓出 "xx市" 和 "xx區"
df_all['city'] = df_all['address'].str.extract(r'(\w+市)')
df_all['district'] = df_all['address'].str.extract(r'(..區)')
# df_all['lon'] = df_all['lon'].astype(float)

df_all['city'] = df_all['city'].str[:3]
df_all['city'] = df_all['city'].replace('台北市', '臺北市')

# 儲存結果
df_all.to_csv('clean/合併/防空疏散合併.csv', index=False)

