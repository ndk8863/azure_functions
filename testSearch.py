# 国立国会図書館サーチAPI

import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
import os

url = "https://ndlsearch.ndl.go.jp/api/opensearch"
params = {
    "cnt": 5,
    "creator":"夏目"
}

res = requests.get(url,params = params)
xml_data = res.text
root = ET.fromstring(xml_data)
items = []
for item in root.findall(".//item"):
    data = {
        "title": item.findtext("title"),
        "link": item.findtext("link"),
        "creator": item.findtext("{*}creator"),  
        "series": item.findtext("{*}seriesTitle"),
        "publisher": item.findtext("{*}publisher"),
        "date": item.findtext("{*}date"),
        "description": item.findtext("description")
    }
    items.append(data)

df = pd.DataFrame(items)

current_dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir_path = os.path.abspath(os.path.join(current_dir_path,os.pardir))

save_file_path = os.path.join(parent_dir_path,"save/tmp.csv")

df.to_csv(save_file_path,encoding='utf8')

