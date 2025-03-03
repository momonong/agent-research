import openai
import traceback

class Agent:
    def __init__(self, system_prompt=""):
        """
        初始化 Agent，並可傳入一個 system prompt（用來設置背景或角色）。
        """
        self.message = []
        if system_prompt:
            self.message.append({"role": "system", "content": system_prompt})

    def add_message(self, role, content):
        """
        新增一則對話訊息。
        """
        self.message.append({"role": role, "content": content})

    def build_prompt(self):
        """
        將所有對話訊息組合成一個完整的 prompt。
        這裡的組合方式可以根據實際需求進行調整。
        """
        prompt = ""
        for msg in self.message:
            if msg["role"] == "system":
                prompt += "System: " + msg["content"] + "\n"
            elif msg["role"] == "user":
                prompt += "User: " + msg["content"] + "\n"
            elif msg["role"] == "assistant":
                prompt += "Assistant: " + msg["content"] + "\n"
        prompt += "Assistant:"
        return prompt

    def get_repsonse(self):
        """
        調用 API 生成回覆，並將回覆加入對話歷史。
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=self.message,
                # max_tokens=1000,
                stream=False,
            )
            answer = response.choices[0].text.strip()
            self.add_message("assistant", answer)
            return answer
        except Exception as e:
            print("生成回答時發生錯誤：", e)
            traceback.print_exc()  # 印出完整的堆疊訊息
            return "生成回答時發生錯誤，請稍後再試。"

    def chat(self, user_input):
        """
        與使用者進行對話，接收使用者輸入，添加到歷史中，並生成回覆。
        """
        self.add_message("user", user_input)
        return self.get_repsonse()
