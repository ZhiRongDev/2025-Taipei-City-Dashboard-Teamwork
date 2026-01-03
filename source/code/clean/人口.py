import os
import glob
import pandas as pd

# 設定資料夾路徑
folder = 'raw/人口統計'

# 搜尋所有 .csv 檔案
csv_files = glob.glob(os.path.join(folder, '*.csv'))

# 讀取並合併所有檔案
dfs = []
for file in csv_files:
    df = pd.read_csv(file, encoding='utf-8', low_memory=False, header=1)
    df = df[df['縣市名稱'].isin(['臺北市', '新北市'])]
    dfs.append(df)
    

merged_df = pd.concat(dfs, ignore_index=True)

# 儲存合併後的檔案
merged_df.to_csv('clean/合併/merged_population.csv', index=False, encoding='utf-8-sig')