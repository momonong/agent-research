import traceback

class Agent():
    def __init__(self, client, system_prompt=""):
        """
        初始化 Agent，接收 AzureOpenAI 客戶端和可選的 system prompt。
        """
        self.client = client
        self.message = [{"role": "system", "content": system_prompt}]
        if system_prompt:
            self.add_message("system", system_prompt)
    
    def add_message(self, role, content):
        """
        新增對話訊息。
        """
        self.message.append({"role": role, "content": content})

    def get_response(self):
        """
        取得回應。
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.message
            )
            # print(response)
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
        return self.get_response()
    
if __name__ == '__main__':
    from src.config import init_openai_client
    client = init_openai_client()
    print("AzureOpenAI client initialized.")
    system_prompt = "You are a helpful assistant."
    agent = Agent(client, system_prompt=system_prompt)
    
    # 範例對話
    user_input = "Does Azure OpenAI support customer managed keys?"
    print("用戶:", user_input)
    answer = agent.chat(user_input)
    print("Agent 回答：", answer)