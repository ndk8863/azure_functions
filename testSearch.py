# 国立国会図書館サーチAPI

import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
from datetime import datetime,timedelta

mediaType = 'books'
# 調査候補
# periodicals
publisher = '講談社'
items = []

url = "https://ndlsearch.ndl.go.jp/api/opensearch"
current = datetime.now()

yyyymm = current.strftime("%Y-%m")
yyyymmddhhmmss = current.strftime("%Y%m%d%H%M%S")
params = {
    "cnt": 500,
    "dpid":"jpro",
    "from":yyyymm,
    "mediatype":mediaType,
    "publisher":publisher

}
try:
    res = requests.get(url,params = params,timeout=20)
except requests.exceptions.Timeout:
    print("タイムアウトが発生しました")
    print(f"パラメータ:{params}")


if res.status_code == 200:
    xml_data = res.text
    root = ET.fromstring(xml_data)
else:
    print(f"月度:{yyyymm}の取得に失敗しました",res.status_code)


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
print(f'月度:{yyyymm}')

df = pd.DataFrame(items)

current_dir_path = os.path.dirname(os.path.abspath(__file__))
parent_dir_path = os.path.abspath(os.path.join(current_dir_path,os.pardir))

save_file_path = os.path.join(parent_dir_path,f"save/{mediaType}_{publisher}_{yyyymmddhhmmss}.csv")

df.to_csv(save_file_path,encoding='utf8')

