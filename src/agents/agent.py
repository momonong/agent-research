import logging
from src.clients.model_client import init_model_client
from src.agents.reasoning import (
    generate_reasoning,
    parse_reasoning_text,
    generate_final_answer,
)
from src.agents.function_registry import (
    get_function_definitions,
    handle_function_call,
    get_function_call_info,
)

logging.basicConfig(level=logging.DEBUG)  # 或設定到合適的等級


class Agent:
    def __init__(self, client, default_source: str = None):
        """
        初始化 Agent，接收外部模型客戶端、系統提示和預設來源（default_source）。
        """
        system_prompt = f"""
        你是一個具有內部推理能力且高效的智慧助手。
        當你接收到問題後，請先詳細描述你的思考過程，
        每個步驟請以「<step1>」、「<step2>」、「<step3>」等格式分隔並記錄。
        請逐步展示這些推理步驟給使用者，
        然後根據這些步驟生成最終答案。
        如果你認為你沒有足夠的資訊直接回答問題，
        請啟用外部搜尋功能以補充資料，
        再根據搜集到的資訊給出最終答案。
        """
        self.client = client
        self.messages = [{"role": "system", "content": system_prompt}]
        self.default_source = default_source
        self.reasoning_steps = []  # 用於記錄模型的推理過程（面向使用者顯示）
        if system_prompt:
            self.add_message("system", system_prompt)

    def add_message(self, role, content):
        """
        新增對話訊息，若不是用戶訊息，則同時記錄到 reasoning_steps 中，
        這裡我們希望呈現給使用者的「思考過程」是比較自然的描述，而非內部調試細節。
        """
        self.messages.append({"role": role, "content": content})
        # 對於非用戶訊息，我們將其記錄下來，但可以過濾或轉換後再記錄
        if role != "user":
            self.reasoning_steps.append(content)

    def chat_stream(self, user_input):
        logging.debug("開始 chat_stream, user_input: %s", user_input)
        # 清空之前的推理紀錄
        self.reasoning_steps = []
        self.add_message("user", user_input)
        yield {"role": "user", "content": user_input}
        logging.debug("已 yield user 訊息")

        # Step 1: 調用模型生成推理過程
        functions = get_function_definitions()
        logging.debug("開始生成推理過程, functions: %s", functions)
        raw_reasoning = generate_reasoning(self.client, user_input, functions)
        logging.debug("raw_reasoning: %s", raw_reasoning)
        steps = parse_reasoning_text(raw_reasoning)
        logging.debug("解析後的 steps: %s", steps)
        for step in steps:
            self.reasoning_steps.append(step)
            logging.debug("yield 推理步驟: %s", step)
            yield {"role": "system", "content": step}

        # Step 2: 使用整個推理過程生成最終答案
        full_reasoning = "\n".join(steps)
        logging.debug("開始生成最終答案，full_reasoning: %s", full_reasoning)
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            functions=functions,
            function_call="auto",
            temperature=0.7,
        )
        logging.debug("模型回應 response: %s", response)

        # 檢查模型回應是否包含 function_call
        info = get_function_call_info(response)
        logging.debug("function call info: %s", info)
        if info:
            logging.debug("進入 function call 處理")
            final_result = yield from handle_function_call(
                response, self.reasoning_steps, self.default_source
            )
            logging.debug("function call 處理結果: %s", final_result)
            if final_result:
                self.add_message("assistant", final_result)
                yield {"role": "assistant", "content": final_result}
                return

        # 如果沒有 function_call，則直接使用模型生成的答案
        content = response.choices[0].message.content.strip()
        logging.debug("直接生成的答案 content: %s", content)
        if content:
            answer = content.strip()
            self.reasoning_steps.append(f"模型直接生成回答：{answer}")
            logging.debug("yield assistant answer: %s", answer)
            yield {"role": "assistant", "content": answer}
            self.add_message("assistant", answer)
            yield {"role": "system", "content": f"最終答案：{answer}"}
        else:
            logging.debug("模型未返回答案")
            yield {"role": "assistant", "content": "模型未返回任何答案。"}

        # 也可以選擇將整個推理過程作為上下文，再生成一個最終答案：
        final_answer = generate_final_answer(self.client, user_input, full_reasoning)
        logging.debug("生成第二個最終答案: %s", final_answer)
        yield {"role": "assistant", "content": final_answer}

    def chat(self, user_input):
        """
        封裝 chat_stream，並將所有生成的訊息合併為最終答案，
        這裡僅用於測試。實際上，您可能會通過 WebSocket 或 SSE 來流式傳輸。
        """
        final_messages = []
        for message in self.chat_stream(user_input):
            # print(message)  # 除錯時印出
            final_messages.append(message)
        return final_messages[-1]["content"]


if __name__ == "__main__":
    from src.clients.model_client import init_model_client

    client = init_model_client()
    system_prompt = "你是一個具有內部推理能力的助手。當你無法直接回答問題時，請啟用外部搜尋並將搜尋過程與最終答案展示給使用者。"
    agent = Agent(client, system_prompt=system_prompt, default_source=None)

    user_input = "請問最新的人工智慧新聞有哪些？"
    print("用戶:", user_input)
    for message in agent.chat_stream(user_input):
        print(message)
