import pandas as pd

# 讀取原始資料
df = pd.read_csv(r'raw\AED位置資訊_20250531.csv')

# 1. 篩選需要欄位
cols = ["場所名稱", "場所縣市", "場所區域", "場所地址", "場所分類", "場所類型", "地點LAT", "地點LNG"]
df = df[cols]

# 2. 篩選場所縣市為臺北市或新北市
df = df[df["場所縣市"].isin(["臺北市", "新北市"])]

# 儲存結果
df.to_csv('clean/合併/AED_list.csv', index=False, encoding='utf-8-sig')
