import azure.functions as func
import azure.durable_functions as df # pyright: ignore[reportMissingImports]
import logging
import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
from datetime import datetime,timedelta
import time


myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

publisher_list = [
        '集英社',
        '講談社',
        '小学館',
        'KADOKAWA',
        '白泉社',
        'スクウェア・エニックス',
        '秋田書店',
        '双葉社',
        '竹書房',
        '芳文社'
    ]

def save_current_media_data(mediaType,publisher):

    mediaType = 'books'
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

    time.sleep(5)



# クライアント関数: HTTPトリガーで定義され、リクエストURLに応じたオーケストレーター関数の起動および、クライアントへのレスポンスを応答
@myApp.route(route="orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    instance_id = await client.start_new(function_name)
    response = client.create_check_status_response(req, instance_id)
    return response

# オーケストレーター関数: アクティビティ関数を呼び出し、管理する
# この例だと3つのアクティビティ関数を実行しており、3つの実行がすべて完了してからレスポンスを応答するようになっています

@myApp.orchestration_trigger(context_name="context")
def save_current_book_orchestrator(context):
    yield context.call_activity("save_current_books_syueisha", "集英社")
    yield context.call_activity("save_current_books_kodansha", "講談社")
    yield context.call_activity("save_current_books_shogakukan", "小学館")
    yield context.call_activity("save_current_books_kadokawa", "KADOKAWA")
    yield context.call_activity("save_current_books_hakusensha", "白泉社")
    yield context.call_activity("save_current_books_square_enix", "スクウェア・エニックス")
    yield context.call_activity("save_current_books_akita", "秋田書店")
    yield context.call_activity("save_current_books_futabasha", "双葉社")
    yield context.call_activity("save_current_books_takeshobo", "竹書房")
    yield context.call_activity("save_current_books_houbunsha", "芳文社")

# アクティビティ関数: 実際のビジネスロジックを定義:この例だと`Hello {都市の名前}`を応答 
@myApp.activity_trigger(input_name="city")
def hello(city: str):
    content = f"Hello {city}"
    return f"{content} How are you?"

@myApp.activity_trigger(input_name="city")
def otukare(city: str):
    content = f"otukare {city}"
    return f"{content} genki?"

@myApp.activity_trigger(input_name="city")
def ohayou(city: str):
    content = f"ohayou {city}"
    return f"{content} ?"

@myApp.activity_trigger(input_name="publisher")
def save_current_books_syueisha(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_kodansha(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_shogakukan(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_kadokawa(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_hakusensha(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_square_enix(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_akita(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_futabasha(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_takeshobo(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)

@myApp.activity_trigger(input_name="publisher")
def save_current_books_houbunsha(publisher):
    mediaType='books'
    save_current_media_data(mediaType,publisher)