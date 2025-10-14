# 国立国会図書館サーチAPI

import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
import os

mediaType = "scores"

url = "https://ndlsearch.ndl.go.jp/api/opensearch"
params = {
    "cnt": 500,
    "mediatype":mediaType
    
}

res = requests.get(url,params = params)
xml_data = res.text
root = ET.fromstring(xml_data)
items = []
for item in root.findall(".//item"):
    data = {
        "title": item.findtext("title"),
        "link": item.findtext("link"),
        "description": item.findtext("description"),
        "pubDate": item.findtext("pubDate"),
        "dc_title": item.findtext("{*}title"),
        "dcndl_titleTranscription>": item.findtext("{*}titleTranscription"),
        "creator": item.findtext("{*}creator"),
        "dcndl_creatorTranscription": item.findtext("{*}creatorTranscription"),
        "dcndl_seriesTitle": item.findtext("{*}seriesTitle"),
        "publisher": item.findtext("{*}publisher"),
        "digitized_publisher": item.findtext("{*}digitized_publisher"),
        "dc_date": item.findtext("{*}date"),
        "dcterms_issued": item.findtext("{*}issued"),
        "dc_subject": item.findtext("{*}subject")
    }
    items.append(data)

df = pd.DataFrame(items)

current_dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir_path = os.path.abspath(os.path.join(current_dir_path,os.pardir))

save_file_path = os.path.join(parent_dir_path,f"save/temp_{mediaType}.csv")

df.to_csv(save_file_path,encoding='utf8')

