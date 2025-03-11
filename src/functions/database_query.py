import json


def query_database(query):
    """
    模擬資料庫查詢函數。
    根據輸入的查詢 key 返回對應資料。
    這裡使用一個靜態字典來模擬資料庫。
    """
    database = {
        "user:1001": {"name": "Alice", "age": 30, "email": "alice@example.com"},
        "user:1002": {"name": "Bob", "age": 25, "email": "bob@example.com"},
        "order:2001": {"item": "Laptop", "price": 1200, "status": "shipped"},
        "order:2002": {"item": "Smartphone", "price": 800, "status": "processing"},
    }
    # 假設 query 是一個 key，例如 "user:1001" 或 "order:2002"
    return database.get(query, "No data found.")


def handle_function_call(response):
    """
    處理模型返回的 function_call 回應。
    如果模型決定調用函數，則解析函數名稱與參數，
    並執行對應的函數，返回執行結果。
    """
    if response.choices[0].finish_reason == "function_call":
        function_call = response.choices[0].message.get("function_call")
        if not function_call:
            return None

        func_name = function_call.get("name")
        # 將 arguments（JSON 字串）解析成字典
        arguments = json.loads(function_call.get("arguments", "{}"))

        if func_name == "query_database":
            result = query_database(arguments.get("query", ""))
            return result

    return None


if __name__ == '__main__':
    fake_response = {
        "choices": [{
            "finish_reason": "function_call",
            "message": {
                "function_call": {
                    "name": "query_database",
                    "arguments": json.dumps({"query": "user:1001"})
                }
            }
        }]
    }
    
    # 模擬一個簡單的回應類
    class FakeChoice:
        def __init__(self, finish_reason, message):
            self.finish_reason = finish_reason
            self.message = message

    class FakeResponse:
        def __init__(self, choices):
            self.choices = choices

    fake_resp_obj = FakeResponse([FakeChoice("function_call", fake_response["choices"][0]["message"])])
    result = handle_function_call(fake_resp_obj)
    print("函數執行結果：", result)