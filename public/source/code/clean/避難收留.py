"""
合併門牌地址欄位
並清理不完整地址
"""
import pandas as pd
import re

# 讀取 CSV 檔案
df = pd.read_csv(r'raw\避難收留\114年臺北市可供避難收容處所一覽表-1140115.csv')

# 假設門牌地址欄位名稱為 '門牌地址'
address_col = '門牌地址'

# 篩選不包含 "市" 和 "區" 的地址
def is_incomplete_address(addr):
    # 檢查是否同時包含 "市" 和 "區"
    return not (re.search(r'市', str(addr)) and re.search(r'區', str(addr)))

# 合併 "縣市"、"鄉鎮"、"村里"、"門牌地址" 欄位為新地址欄位
def merge_address(row):
    parts = []
    for col in ['縣市', '鄉鎮', '村里', address_col]:
        if col in row and pd.notnull(row[col]):
            parts.append(str(row[col]))
    return ''.join(parts)

# 建立新欄位 '完整地址'
df['完整地址'] = df.apply(
    lambda row: merge_address(row) if is_incomplete_address(row[address_col]) else row[address_col],
    axis=1
)

# 移除所有欄位中的換行符號
df = df.applymap(lambda x: str(x).replace('\n', '').replace('\r', '') if pd.notnull(x) else x)

df.to_csv(r'raw/避難收留/114年臺北市可供避難收容處所一覽表-1140115_cleaned.csv', index=False)

# 合併取得經緯度後的雙北資料 =====================================================================


"""
讀取 raw\避難收留\114年臺北市可供避難收容處所一覽表-1140115_cleaned_經緯度.csv 為 df_taipei

讀取 raw\避難收留\新北市避難收容處所一覽表_經緯度.csv  為 df_newtaipei

df_taipei 的欄位如下:
收容所編號,名稱,縣市,鄉鎮,村里,門牌地址,類型,水災,震災,土石流,海嘯,救濟支站,無障礙設施,室內,室外,服務里別,容納人數,收容所面積（平方公尺）,聯絡人姓名,聯絡人連絡電話,管理人姓名,管理人連絡電話,備考,完整地址,longitude,latitude

df_newtaipei 的欄位如下:
serialnumber,provide_contain,provide_shelter,provide_goods,no,countycode,name,district,areacode,village,address,floor,service_village,contact_person,contact_cellphone,suit_for_weak,person,floorspacebuildingothers,floorspacebuildingfactory,suit_for_flood,suit_for_mudflow,suit_for_eqrthquake,suit_for_tsunami,standing_shelter,longitude,latitude
欄位資訊為: serialnumber(序號)、provide_contain(提供收容所功能)、provide_shelter(提供避難所功能)、provide_goods(提供物資點功能)、no(編號)、countycode(縣市代碼)、name(名稱)、district(所在區)、areacode(縣市行政區代碼)、village(所在里別)、address(地址)、floor(所在樓層)、service_village(服務里別)、contact_person(聯絡人)、contact_cellphone(手機)、suit_for_weak(是否適合避難弱者安置)、person(收容人數合計)、floorspacebuildingothers(室內可收容面積)、floorspacebuildingfactory(室外可收容面積)、suit_for_flood(適用水災)、suit_for_mudflow(適用土石流)、suit_for_eqrthquake(適用震災)、suit_for_tsunami(適用海嘯)、standing_shelter(常設避難收容處所)

請比較兩者欄位名稱並進行對應，將 df_newtaipei 的欄位名稱改為與 df_taipei 相同的格式。並合併兩個表格，如欄位缺少，則留空。

"""
# 讀取資料
import os
import pandas as pd
df_taipei = pd.read_csv(r'raw\避難收留\114年臺北市可供避難收容處所一覽表-1140115_cleaned_經緯度.csv')
df_newtaipei = pd.read_csv(r'raw\避難收留\新北市避難收容處所一覽表_經緯度.csv')

# 欄位對應表 (新北英文 -> 台北中文)
col_map = {
    'serialnumber': '收容所編號',
    'name': '名稱',
    'countycode': '縣市',
    'district': '鄉鎮',
    'village': '村里',
    'address': '門牌地址',
    # '類型' 無直接對應
    'suit_for_flood': '水災',
    'suit_for_eqrthquake': '震災',
    'suit_for_mudflow': '土石流',
    'suit_for_tsunami': '海嘯',
    'standing_shelter': '救濟支站',
    # '無障礙設施' 無直接對應
    # '室內', '室外' 無直接對應
    'service_village': '服務里別',
    'person': '容納人數',
    # '收容所面積（平方公尺）' 由 'floorspacebuildingothers' + 'floorspacebuildingfactory' 合併
    'contact_person': '聯絡人姓名',
    'contact_cellphone': '聯絡人連絡電話',
    # '管理人姓名', '管理人連絡電話' 無直接對應
    # '備考' 無直接對應
    # '完整地址' 可用 '縣市'+'鄉鎮'+'村里'+'門牌地址' 合併
    'longitude': 'longitude',
    'latitude': 'latitude'
}

# 依照台北市欄位順序建立新北市資料
newtaipei_renamed = pd.DataFrame()
for col in df_taipei.columns:
    if col in col_map.values():
        # 找到對應的英文欄位
        eng_col = [k for k, v in col_map.items() if v == col]
        if eng_col and eng_col[0] in df_newtaipei.columns:
            newtaipei_renamed[col] = df_newtaipei[eng_col[0]]
        else:
            newtaipei_renamed[col] = None
    elif col == '收容所面積（平方公尺）':
        area = pd.to_numeric(df_newtaipei.get('floorspacebuildingothers', 0), errors='coerce').fillna(0) + \
               pd.to_numeric(df_newtaipei.get('floorspacebuildingfactory', 0), errors='coerce').fillna(0)
        newtaipei_renamed[col] = area
    elif col == '完整地址':
        addr = (
            df_newtaipei.get('countycode', '').astype(str) +
            df_newtaipei.get('district', '').astype(str) +
            df_newtaipei.get('village', '').astype(str) +
            df_newtaipei.get('address', '').astype(str)
        )
        newtaipei_renamed[col] = addr
    else:
        newtaipei_renamed[col] = None

newtaipei_renamed['縣市'] = '新北市'  # 新北市固定值

# 合併兩個表格
df_merged = pd.concat([df_taipei, newtaipei_renamed], ignore_index=True)

df_merged = df_merged.applymap(lambda x: str(x).replace('\n', '').replace('\r', '') if pd.notnull(x) else x)# 儲存合併後的結果
df_merged.to_csv(r'clean/合併/避難收容處所合併.csv', index=False)


for city, folder in [('臺北市', '台北'), ('新北市', '新北')]:
    city_df = df_merged[df_merged['縣市'] == city]
    if not city_df.empty:
        output_path = f'clean/{folder}/避難收容處所合併_{folder}.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        city_df.to_csv(output_path, index=False)