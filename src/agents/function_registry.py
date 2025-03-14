def get_function_registry(query: str) -> list:
    """
    根據查詢內容返回適用的 function registry.
    這裡暫時固定返回兩個定義：search_website 與 query_database。
    你可以根據 query 調整返回內容。
    """
    return [
        {
            "name": "search_website",
            "description": "在成功大學國際處網站搜尋相關資訊。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用於搜尋的查詢詞。"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "query_database",
            "description": "模擬資料庫查詢，根據查詢 key 返回對應的資料。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要查詢的關鍵字。"
                    }
                },
                "required": ["query"]
            }
        }
    ]
