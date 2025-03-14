import traceback
from src.tools.preferred_answers import load_google_sheet, get_preferred_answer
from src.functions.database_query import handle_function_call
from src.agents.function_registry import (
    get_function_definitions,
    get_function_call_info,
)
from src.functions.web_search import search_web_with_firefox


class Agent:
    def __init__(self, client, system_prompt="", default_source: str = None):
        """
        初始化 Agent，接收 AzureOpenAI 客戶端和可選的 system prompt。
        """
        self.client = client
        self.message = [{"role": "system", "content": system_prompt}]
        # 讀取預設回答資料（從 Google Sheet 載入）
        self.google_sheet = load_google_sheet()
        # 如果有特定的來源限制，可設置在這裡
        self.default_source = default_source

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
        # 1. 嘗試從預設回答中取得答案
        preferred = get_preferred_answer(query, self.google_sheet)
        if preferred:
            self.add_message("assistant", preferred)
            return preferred

        # 2. 根據查詢決定是否啟用 function calling
        functions = []
        functions = get_function_definitions()

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # 根據你的部署名稱調整
                messages=self.message,
                functions=functions if functions else None,
                function_call="auto" if functions else None,
            )
            # 3. 檢查是否返回了 function_call
            info = get_function_call_info(response)
            if info and info["func_name"] == "search_website":
                query = info["arguments"].get("query", "")
                # 調用 search_website 函數，注意可傳入 default_source 限定來源
                result = search_web_with_firefox(query, source_url=self.default_source)
                self.add_message("assistant", str(result))
                return str(result)

            # 4. 如果沒有 function_call，則直接返回模型生成的答案
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


if __name__ == "__main__":
    from src.clients.chat_client import init_chat_model_client
    client = init_chat_model_client()
    system_prompt = "你是一個具有函數調用能力的助手，當無法直接回答時會從網路搜尋最新資訊並整合摘要返回。"
    # 這裡 default_source 可選，若無，則會根據搜尋引擎自動構造 URL（例如 Google 搜尋或 Bing 搜尋）
    agent = Agent(client, system_prompt=system_prompt, default_source=None)
    
    user_input = "請問最新的人工智慧新聞有哪些？"
    print("用戶:", user_input)
    answer = agent.chat(user_input)
    print("Agent 回答：", answer)
