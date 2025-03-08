# tests/test_function_calling.py
import json
import unittest
from src.clients.functions.database_query import query_database, handle_function_call

class FakeChoice:
    def __init__(self, finish_reason, message):
        self.finish_reason = finish_reason
        self.message = message

class FakeResponse:
    def __init__(self, choices):
        self.choices = choices

class TestFunctionCalling(unittest.TestCase):
    def test_query_database_direct(self):
        # 直接測試 query_database 函數
        result = query_database("user:1001")
        # 測試返回值是否包含預期的姓名，這裡測試 "Alice"
        self.assertEqual(result, {"name": "Alice", "age": 30, "email": "alice@example.com"})
    
    def test_handle_function_call(self):
        # 模擬一個帶有 function_call 的 response
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
        
        # 建立假回應物件
        fake_resp_obj = FakeResponse([
            FakeChoice("function_call", fake_response["choices"][0]["message"])
        ])
        
        result = handle_function_call(fake_resp_obj)
        # 驗證返回的結果應該是 user:1001 對應的資料
        self.assertEqual(result, {"name": "Alice", "age": 30, "email": "alice@example.com"})

if __name__ == '__main__':
    unittest.main()
