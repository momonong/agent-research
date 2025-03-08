import traceback
from src.tools.preferred_answers import load_google_sheet, get_preferred_answer
from src.clients.functions.database_query import handle_function_call

class Agent():
    def __init__(self, client, system_prompt=""):
        """
        初始化 Agent，接收 AzureOpenAI 客戶端和可選的 system prompt。
        """
        self.client = client
        self.message = [{"role": "system", "content": system_prompt}]
        # 讀取預設回答資料（從 Google Sheet 載入）
        self.google_sheet = load_google_sheet()

        if system_prompt:
            self.add_message("system", system_prompt)
    
    def add_message(self, role, content):
        """
        新增對話訊息。
        """
        self.message.append({"role": role, "content": content})

    def get_response(self, query):
        """
        :param query: 使用者輸入的問題文字
        :return: 回答文字

        流程：
          1. 檢查預設回答資料是否匹配，若有則直接返回。
          2. 若用戶輸入包含關鍵字（例如「復學證明」），則在 API 請求中加入 function calling 的函數定義，
             讓模型有機會調用 query_database 函數進行模擬資料庫查詢。
          3. 若模型返回 function_call，則解析並執行對應函數；否則直接返回模型生成的回答。
        """
        # 若有預設回答，則直接回傳
        preferred = get_preferred_answer(query, self.google_sheet)
        if preferred:
            self.add_message("assistant", preferred)
            return preferred

        # 判斷是否需要加入 function calling（例如，當查詢包含「復學證明」）
        functions = []
        if "復學證明" in query:
            functions = [
                {
                    "name": "query_database",
                    "description": "模擬資料庫查詢，根據查詢 key 返回對應的資料。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "要查詢的關鍵字，例如 '復學證明'。"
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # 根據你的部署名稱調整
                messages=self.message,
                functions=functions if functions else None,
                function_call="auto" if functions else None,
                max_tokens=150,
            )
            # 如果有 function_call，嘗試處理它
            if functions:
                function_result = handle_function_call(response)
                if function_result is not None:
                    self.add_message("assistant", str(function_result))
                    return str(function_result)
            # 否則，返回模型生成的文字回答
            answer = response.choices[0].message.content
            self.add_message("assistant", answer)
            return answer
        except Exception:
            traceback.print_exc()
            return "An error occurred. Please try again."
        
    def chat(self, user_input):
        """
        與使用者對話。
        """
        self.add_message("user", user_input)
        return self.get_response(user_input)
    
if __name__ == '__main__':
    from src.config import init_openai_client
    client = init_openai_client()
    print("AzureOpenAI client initialized.")
    system_prompt = "You are a helpful assistant with function calling capabilities."
    agent = Agent(client, system_prompt=system_prompt)
    
    # 範例對話：查詢「復學證明」的資料
    user_input = "申請復學的居留簽證的時候，需要的復學證明可以什麼時候拿到"
    print("用戶:", user_input)
    answer = agent.chat(user_input)
    print("Agent 回答：", answer)
