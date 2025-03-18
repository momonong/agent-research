import sys

try:
    sys.stdin.reconfigure(encoding='utf-8')
except Exception as e:
    print("無法重新設定 sys.stdin 編碼：", e)

from src.clients.chat_client import init_chat_model_client
from src.agents.agent import Agent

def main():
    client = init_chat_model_client()
    system_prompt = "你是一個智慧且自信的助手。如果你對問題有充分的資訊，請直接回答；如果你不確定，或者認為需要額外資訊來提供正確回答，請返回一個 function_call 來調用外部搜尋功能。"
    agent = Agent(client, system_prompt=system_prompt, default_source=None)
    
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
