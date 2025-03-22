import json
from src.functions.web_search import search_web_with_firefox
from src.tools.get_current_time import get_current_time
from src.functions.summarize_result import summarize_result

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
        },
        {
            "name": "get_current_time",
            "description": "返回當前系統時間。",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    ]


def get_function_call_info(response) -> dict:
    """
    從模型返回的 response 中提取 function_call 的相關資訊。
    """
    if response.choices[0].finish_reason != "function_call":
        return 

    function_call = response.choices[0].message.function_call
    if not function_call:
        return 

    func_name = function_call.name
    arguments = json.loads(function_call.arguments)
    return {"func_name": func_name, "arguments": arguments}


async def handle_function_call(response, reasoning, default_source: str = None):
    """
    處理模型返回的 function_call 回應：
      - 如果函數名稱為 "search_website"，則調用 search_web_with_firefox 並利用 summarize_result 整合結果；
      - 如果函數名稱為 "get_current_time"，則調用 get_current_time 返回當前時間。
    以生成器方式逐步 yield 處理訊息，最終返回結果。
    """
    info = get_function_call_info(response)
    if not info:
        return

    # 處理搜尋功能
    if info["func_name"] == "search_website":
        reasoning.append(
            f"模型返回 function_call，準備執行 'search_website'，參數："
            + json.dumps(info["arguments"], ensure_ascii=False)
            + json.dumps(info["arguments"], ensure_ascii=False)
        )
        yield {
            "message": f"模型返回 function_call，進行網路搜尋。",
            "finalized": False,
            "reasoning": [reasoning.copy()[-1]],  # 複製一份當前推理過程
            "source": "search_website1",
        }
        query_arg = info["arguments"].get("query", "")
        # 呼叫搜尋函數取得原始結果
        raw_results = await search_web_with_firefox(query_arg, source_url=default_source)
        reasoning.append(f"搜尋結果：" + json.dumps(raw_results, ensure_ascii=False))
        yield {
            "message": f"網路搜尋完成。",
            "finalized": False,
            "reasoning": [reasoning.copy()[-1]],
            "source": "search_website2",
        }
        # 使用 summarize_search_sresult 將原始結果與推理過程整合摘要
        summary = summarize_result(
            {
                "raw_search_results": raw_results,
                "reasoning": reasoning,
            },
        )
        reasoning.append(f"將搜尋結果進行統整。")
        yield {
            "message": summary,
            "finalized": True,
            "reasoning": [reasoning.copy()[-1]],  # 傳回完整的推理過程
            "source": "search_website3",
        }
        return 

    if info["func_name"] == "get_current_time":
        reasoning.append(f"模型返回 function_call，執行 'get_current_time'。")
        yield {
            "message": "模型返回 function_call，取得當前時間。",
            "finalized": False,
            "reasoning": [reasoning.copy()[-1]],
            "source": "get_current_time1",
        }
        current_time = get_current_time()
        summary = summarize_result(
            {
                "current_time": current_time,
                "reasoning": reasoning,
            },
        )
        reasoning.append(f"{summary}")
        yield {
            "message": f"{summary}",
            "finalized": True,
            "reasoning": [reasoning.copy()[-1]],
            "source": "get_current_time2",
        }
        return 
    
    return
