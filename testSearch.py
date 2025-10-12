# 国立国会図書館サーチAPI

import requests
import xml.etree.ElementTree as ET
import json
url = "https://ndlsearch.ndl.go.jp/api/opensearch"
params = {
    "cnt": 5,
    "creator":"夏目"
}

res = requests.get(url,params = params)
xml_data = res.text
# res = requests.get(url)
# data = res.json()
# print(data)
print(xml_data)

root = ET.fromstring(xml_data)

items = []

for item in root.findall(".//item"):
    data = {
        "title": item.findtext("title"),
        "link": item.findtext("link"),
        "creator": item.findtext("{*}creator"),  # 名前空間があるので{*}でマッチ
        "series": item.findtext("{*}seriesTitle"),
        "publisher": item.findtext("{*}publisher"),
        "date": item.findtext("{*}date"),
        "description": item.findtext("description")
    }
    items.append(data)

json_output = json.dumps(items,ensure_ascii=False,indent=2)
print(json_output)

# for item in data["response"]["items"]:
#     print(item["title"],"-",item.get("creator","不明"))