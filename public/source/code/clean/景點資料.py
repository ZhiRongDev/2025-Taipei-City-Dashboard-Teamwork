import pandas as pd



df = pd.read_csv(r'raw\景點\歷年國內主要觀光遊憩據點遊客人數月別統計.csv', encoding='utf-8')
df_select = df[df['縣市'].isin(['臺北市', '新北市'])]
df_select.to_csv('clean/合併/spot_flow_month.csv', index=None)

df_select = df_select.drop(columns=['1月', '2月', '3月', '4月', '5月',
       '6月', '7月', '8月', '9月', '10月', '11月', '12月'])  # 刪除 '縣市' 欄位


df_select = df_select[['類型', '觀光遊憩區', '細分', '縣市', '縣市別']].drop_duplicates()

df_select['name'] = df_select['縣市'] + df_select['細分']
df_select['space_name'] = df_select['縣市'] + ' ' + df_select['細分']

df_select.to_csv('clean/合併/spot_list.csv', index=None)

