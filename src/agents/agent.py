import traceback
from src.tools.preferred_answers import load_google_sheet, get_preferred_answer

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

        先檢查預設回答資料中是否有匹配答案，
        如果有則直接返回預設回答，
        否則使用 AzureOpenAI 的 Chat API 生成回答。
        """
        # 若有預設回答，則直接回傳
        preferred = get_preferred_answer(query, self.google_sheet)
        if preferred:
            self.add_message("assistant", preferred)
            return preferred
        
        # 使用 AzureOpenAI 生成回答
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
        return self.get_response(user_input)
    
if __name__ == '__main__':
    from src.config import init_openai_client
    client = init_openai_client()
    print("AzureOpenAI client initialized.")
    system_prompt = "You are a helpful assistant."
    agent = Agent(client, system_prompt=system_prompt)
    
    # 範例對話
    # user_input = "Does Azure OpenAI support customer managed keys?"
    # 範例預設對話
    user_input = "申請復學的居留簽證的時候需要的復學證明可以什麼時候拿到"
    print("用戶:", user_input)
    answer = agent.chat(user_input)
    print("Agent 回答：", answer)