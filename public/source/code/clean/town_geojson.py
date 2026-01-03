import json

with open('raw/人口統計/geodata/113人口統計_鄉鎮市區.geojson', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 你可以在這裡進一步處理 geojson_data
print(geojson_data.keys())
# 台北
filtered_features = [
    feature for feature in geojson_data['features']
    if feature['properties']['COUNTY'] in ['臺北市']
]
# print(f"Filtered features count: {len(filtered_features)}")

geojson_data['features'] = filtered_features

# with open('town_pretty.geojson', 'w', encoding='utf-8') as f:
#     json.dump(geojson_data, f, ensure_ascii=False, indent=4)

with open(r'clean\台北\town_taipei.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False)

# 新北
filtered_features = [
    feature for feature in geojson_data['features']
    if feature['properties']['COUNTY'] in ['新北市']
]

geojson_data['features'] = filtered_features

with open(r'clean\新北\town_newtaipei.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False)