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

    async def chat_stream(self, user_input):
        logging.debug("開始 chat_stream, user_input: %s", user_input)
        # 清空之前的推理紀錄
        self.reasoning_steps = []
        self.add_message("user", user_input)
        yield {"message": user_input, "finalized": False, "source": "UserInput"}
        logging.debug("已 yield user 訊息")

        # Step 1: 調用模型生成推理過程
        functions = get_function_definitions()
        logging.debug("開始生成推理過程, functions: %s", functions)
        raw_reasoning = generate_reasoning(self.client, user_input, functions)
        logging.debug("raw_reasoning: %s", raw_reasoning)
        steps = parse_reasoning_text(raw_reasoning)
        logging.debug("解析後的 steps: %s", steps)
        for step in steps:
            if not step.strip():  # 跳過空消息
                continue
            self.reasoning_steps.append(step)
            logging.debug("yield 推理步驟: %s", step[-1])
            yield {"reasoning": [step], "finalized": False, "source": "ReasoningStep"}

        # Step 2: 使用整個推理過程生成最終答案
        full_reasoning = "\n".join(steps)
        logging.debug("開始生成最終答案，full_reasoning: %s", full_reasoning)
        self.add_message("system", f"這是你可以參考的推理步驟: {full_reasoning}，生成不包含推理步驟的最終答案。")
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
            async for item in handle_function_call(
                response, self.reasoning_steps, self.default_source
            ):
                item["source"] = "FunctionCall"
                yield item
            return

        # 如果沒有 function_call，則直接使用模型生成的答案
        content = response.choices[0].message.content.strip()
        logging.debug("直接生成的答案 content: %s", content)
        if content:
            answer = content.strip()
            logging.debug("yield assistant answer: %s", answer)
            self.add_message("assistant", answer)
            yield {"message": answer, "finalized": True, "source": "AssistantAnswer"}
        else:
            logging.debug("模型未返回答案")
            yield {"message": "模型未返回任何答案", "finalized": True, "source": "AssistantAnswer"}


    async def chat(self, user_input):
        """
        封裝 chat_stream，並將所有生成的訊息合併為最終答案，
        這裡僅用於測試。實際上，您可能會通過 WebSocket 或 SSE 來流式傳輸。
        """
        final_messages = []
        async for msg in self.chat_stream(user_input):
            final_messages.append(msg)
        return final_messages[-1]["message"]


if __name__ == "__main__":
    from src.clients.model_client import init_model_client

    client = init_model_client()
    system_prompt = "你是一個具有內部推理能力的助手。當你無法直接回答問題時，請啟用外部搜尋並將搜尋過程與最終答案展示給使用者。"
    agent = Agent(client, system_prompt=system_prompt, default_source=None)

    user_input = "請問最新的人工智慧新聞有哪些？"
    print("用戶:", user_input)
    for message in agent.chat_stream(user_input):
        print(message)
