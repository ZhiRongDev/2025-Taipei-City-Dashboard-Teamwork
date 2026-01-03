'''
讀取 clean\AED_list.csv 資料 
1. 篩選出 "場所縣市,場所區域, 場所名稱, 地點LAT, 地點LNG, 場所分類, 場所類型, 場所地址" 欄位 (按順序)
2. 將欄位名稱改成 City, Town, Name, Lat, Lon, Type, Subtype, Address
3. 建立 Source 欄位，值為 "AED"

讀取 clean\消防局資源_Resource_FillCoordinate.csv 資料
1. 篩選出 "cityName,townName,LocationName,lat,lon,單位,address" 欄位 (按順序)
2. 將欄位名稱改成 City, Town, Name, Lat, Lon, Type, Address
3. 建立 Source 欄位，值為 "警消"

讀取 clean\防空疏散合併.csv 資料
1. 篩選出 "city, district, number, lat, lon, category, address" 欄位 (按順序)
2. 將欄位名稱改成 City, Town, Name, Lat, Lon, Type, Address
3. 建立 Source 欄位，值為 "防空疏散地點"

讀取 clean\避難收容處所合併.csv 資料
1. 篩選出 "縣市, 鄉鎮, 名稱, latitude, longitude, 類型, 門牌地址" 欄位 (按順序)
2. 將欄位名稱改成 City, Town, Name, Lat, Lon, Type, Address
3. 建立 Source 欄位，值為 "避難收容所"

合併上述資料並輸出到 merge\town_coordinates_list.csv
'''

import pandas as pd
import os

# 讀取 AED_list.csv
aed_cols = ["場所縣市", "場所區域", "場所名稱", "地點LAT", "地點LNG", "場所分類", "場所類型", "場所地址"]
aed_rename = {
    "場所縣市": "City",
    "場所區域": "Town",
    "場所名稱": "Name",
    "地點LAT": "Lat",
    "地點LNG": "Lon",
    "場所分類": "Type",
    "場所類型": "Subtype",
    "場所地址": "Address"
}
aed = pd.read_csv("clean/AED_list.csv", usecols=aed_cols)
aed = aed.rename(columns=aed_rename)
aed["Source"] = "AED"

# 讀取 消防局資源_Resource_FillCoordinate.csv
fire_cols = ["cityName", "townName", "LocationName", "lat", "lon", "單位", "address"]
fire_rename = {
    "cityName": "City",
    "townName": "Town",
    "LocationName": "Name",
    "lat": "Lat",
    "lon": "Lon",
    "單位": "Type",
    "address": "Address"
}
fire = pd.read_csv("clean/消防局資源_Resource_FillCoordinate.csv", usecols=fire_cols)
fire = fire.rename(columns=fire_rename)
fire["Source"] = "警消"
fire["Subtype"] = ""  # 補齊欄位

# 讀取 防空疏散合併.csv
shelter_cols = ["city", "district", "number", "lat", "lon", "category", "address"]
shelter_rename = {
    "city": "City",
    "district": "Town",
    "number": "Name",
    "lat": "Lat",
    "lon": "Lon",
    "category": "Type",
    "address": "Address"
}
shelter = pd.read_csv("clean/防空疏散合併.csv", usecols=shelter_cols)
shelter = shelter.rename(columns=shelter_rename)
shelter["Source"] = "防空疏散地點"
shelter["Subtype"] = ""  # 補齊欄位

# 讀取 雙北避難收容處所_合併.csv
refuge_cols = ["縣市", "鄉鎮", "名稱", "latitude", "longitude", "類型", "門牌地址"]
refuge_rename = {
    "縣市": "City",
    "鄉鎮": "Town",
    "名稱": "Name",
    "latitude": "Lat",
    "longitude": "Lon",
    "類型": "Type",
    "門牌地址": "Address"
}
refuge = pd.read_csv("clean/避難收容處所合併.csv", usecols=refuge_cols)
refuge = refuge.rename(columns=refuge_rename)
refuge["Source"] = "避難收容所"
refuge["Subtype"] = ""  # 補齊欄位

# 統一欄位順序
columns = ["City", "Town", "Name", "Lat", "Lon", "Type", "Subtype", "Address", "Source"]
aed = aed[columns]
fire = fire[columns]
shelter = shelter[columns]
refuge = refuge[columns]

# 合併
merged = pd.concat([aed, fire, shelter, refuge], ignore_index=True)

# 輸出
os.makedirs("merge", exist_ok=True)
merged.to_csv("merge/town_coordinates_list.csv", index=False, encoding="utf-8-sig")