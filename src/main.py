import sys

try:
    sys.stdin.reconfigure(encoding='utf-8')
except Exception as e:
    print("無法重新設定 sys.stdin 編碼：", e)

from src.clients.model_client import init_model_client
from src.agents.agent import Agent

def main():
    client = init_model_client()
    agent = Agent(client, default_source=None)
    
    print("歡迎使用 Agent 聊天系統！請輸入您的問題，輸入 'exit' 結束。")
    
    while True:
        user_input = input("請輸入您的問題：")
        if user_input.lower() in ["exit", "quit"]:
            print("結束聊天。")
            break
        answer = agent.chat(user_input)
        print("Agent 回答：", answer)
        print("-" * 40)

if __name__ == '__main__':
    main()
