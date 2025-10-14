import azure.functions as func
import azure.durable_functions as df # pyright: ignore[reportMissingImports]
import logging


myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

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
def hello_orchestrator(context):
    result1 = yield context.call_activity("hello", "Seattle")
    result2 = yield context.call_activity("hello", "Tokyo")
    result3 = yield context.call_activity("hello", "London")
    result4 = yield context.call_activity("otukare", "Osaka")
    result5 = yield context.call_activity("ohayou", "Osaka")

    return [result1, result2, result3, result4, result5]

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

# azure functionsのコード
# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# @app.route(route="http_trigger")
# def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )