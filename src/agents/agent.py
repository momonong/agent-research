import traceback
import json
from src.tools.preferred_answers import load_google_sheet, get_preferred_answer
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
        # 用於記錄中間思考過程
        self.chain_of_thought = []
        if system_prompt:
            self.add_message("system", system_prompt)

    def add_message(self, role, content):
        """
        新增對話訊息，同時記錄到 chain_of_thought（除非是用戶訊息）。
        """
        self.message.append({"role": role, "content": content})
        if role != "user":
            self.chain_of_thought.append(f"{role}: {content}")

    def chat_stream(self, user_input):
        """
        以生成器方式處理對話，每完成一步就 yield 一個中間訊息，
        使前端可以實時顯示 Agent 的思考過程。
        """
        # 記錄用戶輸入
        self.add_message("user", user_input)
        yield {"role": "user", "content": user_input}

        # Step 1: 收到查詢
        self.chain_of_thought = []  # 清空之前的記錄
        self.chain_of_thought.append("Step 1: 收到使用者輸入。")
        yield {"role": "system", "content": "Step 1: 收到使用者輸入。"}

        # Step 2: 檢查預設回答
        # preferred = get_preferred_answer(self.google_sheet, user_input)
        preferred = None

        if preferred:
            self.chain_of_thought.append("Step 2: 在預設回答中找到答案。")
            self.add_message("system", preferred)
            yield {"role": "system", "content": preferred}
            return

        self.chain_of_thought.append(
            "Step 2: 預設回答中無合適答案，啟用 function calling。"
        )
        yield {
            "role": "system",
            "content": "Step 2: 預設回答中無合適答案，啟用 function calling。",
        }

        # Step 3: 載入 function definitions
        functions = get_function_definitions()
        self.chain_of_thought.append(
            "Step 3: 載入 function 設定。" + json.dumps(functions)
        )
        yield {"role": "system", "content": "Step 3: 載入 function 設定。"}

        try:
            # Step 4: 呼叫模型 API，讓模型決定是否需要調用 function
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.message,
                functions=functions if functions else None,
                function_call="auto" if functions else None,
            )
            self.chain_of_thought.append("Step 4: 模型回應。")
            yield {"role": "system", "content": "Step 4: 模型回應。"}

            # Step 5: 檢查模型是否返回了 function_call
            info = get_function_call_info(response)
            if info and info["func_name"] == "search_website":
                self.chain_of_thought.append(
                    "Step 5: 模型返回 function_call，準備執行 'search_website'，參數："
                    + json.dumps(info["arguments"])
                )
                yield {
                    "role": "system",
                    "content": "Step 5: 模型返回 function_call，執行搜尋功能。",
                }
                query_arg = info["arguments"].get("query", "")
                result = search_web_with_firefox(
                    query_arg, source_url=self.default_source
                )
                self.chain_of_thought.append("Step 6: 搜尋結果：" + json.dumps(result))
                yield {"role": "system", "content": "Step 6: 搜尋完成。"}
                self.add_message("system", str(result))
                yield {"role": "assistant", "content": "最終答案：" + str(result)}
                return

            # Step 7: 如果沒有 function_call，則使用模型直接生成的答案
            answer = response.choices[0].message.content.strip()
            self.chain_of_thought.append("Step 7: 模型直接回答：" + answer)
            yield {"role": "assistant", "content": answer}
            self.add_message("assistant", answer)
            yield {"role": "system", "content": "最終答案：" + answer}

        except Exception as e:
            traceback.print_exc()
            yield {"role": "system", "content": "處理時發生錯誤：" + str(e)}

    def chat(self, user_input):
        """
        封裝 chat_stream，並將所有生成的訊息合併為最終答案。
        這裡僅用於測試，你也可以將 chat_stream 用於真正的流式傳輸。
        """
        final_messages = []
        for message in self.chat_stream(user_input):
            print(message)
            final_messages.append(message)

        # 此處你可以選擇只返回最終答案，也可以返回整個訊息列表
        return final_messages[-1]["content"]  # 返回最終答案


if __name__ == "__main__":
    from src.clients.chat_client import init_chat_model_client
    client = init_chat_model_client()
    system_prompt = "你是一個具有內部推理能力的助手。在回答問題前，請先展示你的思考過程，然後再給出最終答案。"
    agent = Agent(client, system_prompt=system_prompt, default_source=None)
    
    user_input = "請問最新的人工智慧新聞有哪些？"
    print("用戶:", user_input)
    for message in agent.chat_stream(user_input):
        print(message)