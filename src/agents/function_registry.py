import json
from src.functions.web_search import search_web_with_firefox


def get_function_definitions() -> list:
    """
    根據 query 返回可用的函數定義列表。
    這裡我們固定提供 "search_website" 這個函數。
    """
    # 根據 query 你可以加入判斷，這裡先固定返回 "search_website"
    return [
        {
            "name": "search_website",
            "description": "從網路上搜尋即時資訊，並整理摘要返回答案。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "用於搜尋的查詢詞。"}
                },
                "required": ["query"],
            },
        }
    ]


def get_function_call_info(response) -> dict:
    """
    從模型返回的 response 中提取 function_call 的相關資訊。
    """
    if response.choices[0].finish_reason != "function_call":
        return None

    function_call = response.choices[0].message.function_call
    if not function_call:
        return None
    print(function_call)
    func_name = function_call.name
    arguments = json.loads(function_call.arguments)
    return {"func_name": func_name, "arguments": arguments}


def handle_function_call(response, default_source: str = None) -> str:
    """
    處理模型返回的 function_call 回應：
    如果函數名稱為 "search_website"，則調用 search_web_with_firefox 並返回結果。
    """
    function_call_info = get_function_call_info(response)
    if not function_call_info:
        return None

    if function_call_info["name"] == "search_website":
        query = function_call_info.get("query", "")
        # 這裡我們使用預設的來源 URL（或 default_source，如果有提供）
        return (
            search_web_with_firefox(query, source_url=default_source)[0]["title"]
            if search_web_with_firefox(query, source_url=default_source)
            else "無搜尋結果"
        )

    return None
