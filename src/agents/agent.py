import json
import traceback
from src.clients.chat_client import init_chat_model_client
from src.agents.function_registry import get_function_definitions, handle_function_call

class Agent:
    def __init__(self, client, system_prompt="", default_source: str = None):
        """
        初始化 Agent，接收外部模型客戶端、系統提示和預設來源（default_source）。
        """
        self.client = client
        self.messages = [{"role": "system", "content": system_prompt}]
        self.default_source = default_source
        self.chain_of_thought = []  # 用於記錄模型的推理過程（面向使用者顯示）
        if system_prompt:
            self.add_message("system", system_prompt)

    def add_message(self, role, content):
        """
        新增對話訊息，若不是用戶訊息，則同時記錄到 chain_of_thought 中，
        這裡我們希望呈現給使用者的「思考過程」是比較自然的描述，而非內部調試細節。
        """
        self.messages.append({"role": role, "content": content})
        # 對於非用戶訊息，我們將其記錄下來，但可以過濾或轉換後再記錄
        if role != "user":
            self.chain_of_thought.append(content)

    def chat_stream(self, user_input):
        # 清空之前的推理記錄
        self.chain_of_thought = []
        step = 0
        self.add_message("user", user_input)
        yield {"role": "user", "content": user_input}

        # 收到使用者輸入
        step += 1
        self.chain_of_thought.append(f"Step {step}: 收到使用者輸入。")
        yield {"role": "system", "content": f"Step {step}: 收到使用者輸入。"}

        # 載入 function 定義
        step += 1
        functions = get_function_definitions()
        self.chain_of_thought.append(f"Step {step}: 載入 function 定義：" + json.dumps(functions))
        yield {"role": "system", "content": f"Step {step}: 載入 function 定義。"}

        try:
            # 呼叫模型 API，讓模型決定是否需要調用 function
            response = self.client.chat.completions.create(
                model="gpt-4o",  # 根據你的部署名稱調整
                messages=self.messages,
                functions=functions,
                function_call="auto",
                temperature=0.7,
            )
            step += 1
            self.chain_of_thought.append(f"Step {step}: 模型回應完成。")
            yield {"role": "system", "content": f"Step {step}: 模型回應完成。"}

            # 使用 handle_function_call 處理 function_call 相關流程
            result = yield from handle_function_call(step, response, self.chain_of_thought, self.default_source)
            if result:
                self.add_message("assistant", result)
                return

            # 如果沒有 function_call，則直接使用模型生成的答案
            step += 1
            content = response.choices[0].message.content
            if content:
                answer = content.strip()
                self.chain_of_thought.append(F"Step {step}: 模型直接生成回答：" + answer)
                yield {"role": "assistant", "content": answer}
                self.add_message("assistant", answer)
                yield {"role": "system", "content": "最終答案：" + answer}
            else:
                yield {"role": "assistant", "content": "模型未返回任何答案。"}
        except Exception as e:
            traceback.print_exc()
            yield {"role": "assistant", "content": "處理時發生錯誤：" + str(e)}


    def chat(self, user_input):
        """
        封裝 chat_stream，並將所有生成的訊息合併為最終答案，
        這裡僅用於測試。實際上，您可能會通過 WebSocket 或 SSE 來流式傳輸。
        """
        final_messages = []
        for message in self.chat_stream(user_input):
            print(message)  # 除錯時印出
            final_messages.append(message)
        return final_messages[-1]["content"]

if __name__ == "__main__":
    from src.clients.chat_client import init_chat_model_client
    client = init_chat_model_client()
    system_prompt = "你是一個具有內部推理能力的助手。當你無法直接回答問題時，請啟用外部搜尋並將搜尋過程與最終答案展示給使用者。"
    agent = Agent(client, system_prompt=system_prompt, default_source=None)
    
    user_input = "請問最新的人工智慧新聞有哪些？"
    print("用戶:", user_input)
    for message in agent.chat_stream(user_input):
        print(message)
