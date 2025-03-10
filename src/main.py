from src.config import init_openai_client
from src.agents.agent import Agent

def main():
    client = init_openai_client()
    system_prompt = "You are a helpful assistant."
    agent = Agent(client, system_prompt=system_prompt)
    
    # 範例對話
    user_input = "Does Azure OpenAI support customer managed keys?"
    # 範例預設對話
    # user_input = "復學證明可以什麼時候拿到"
    # user_input = "how to drop out of school"
    # user_input = "is there any scholarships for phd students"
    # user_input = "how to apply for a scholarship"
    print("用戶:", user_input)
    answer = agent.chat(user_input)
    print("Agent 回答：", answer)

if __name__ == '__main__':
    main()
