import pandas as pd
import json

# 讀取 JSON 檔案
with open(r'raw\消防局資源_Resource.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 轉換成 DataFrame
df = pd.DataFrame(data['ResourceLocation'])

df.drop(columns=['ResourceDetail'], inplace=True)
df = df[df['cityName'].isin(['臺北市', '新北市'])]  # 篩選出臺北市和新北市的資料

# 把 LocationName 欄位中字串包含 [消防局、派出所、分局、義勇消防] 的資料過濾出來並新增 '單位' 欄位標註
keywords = ['消防局', '派出所', '分局', '義勇消防']
mask = df['LocationName'].str.contains('|'.join(keywords))
filtered_df = df[mask].copy()
filtered_df['單位'] = filtered_df['LocationName'].apply(
    lambda x: next((k for k in keywords if k in x), '')
)
filtered_df.to_csv('clean/合併/消防局資源_Resource.csv', index=False, encoding='utf-8-sig')