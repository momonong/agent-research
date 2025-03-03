from src.config import OpenAIConfig
from src.agent import Agent


def main():
    # 初始化 API 配置
    config = OpenAIConfig()
    config.init_openai()

    # 設定 system prompt，定義 Agent 的角色或背景
    system_prompt = "你是一個專業的問答助手，請盡可能詳盡地回答問題。"
    agent = Agent(system_prompt=system_prompt)

    # 測試對話
    user_input = "什麼是人工智慧？"
    answer = agent.chat(user_input)
    print("Agent 回答：", answer)


if __name__ == "__main__":
    main()
