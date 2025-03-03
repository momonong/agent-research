# src/config.py
import os
import openai
from dotenv import load_dotenv

class OpenAIConfig:
    def __init__(self):
        load_dotenv()
        self.api_type = "azure"
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = "2024-09-01-preview"
        self.model = "gpt-35-turbo-instruct"  # 預設模型名稱

    def init_openai(self):
        openai.api_type = self.api_type
        openai.api_key = self.api_key
        openai.azure_endpoint = self.azure_endpoint
        openai.api_version = self.api_version

if __name__ == '__main__':
    config = OpenAIConfig()
    config.init_openai()
    print("OpenAI API 配置已初始化")
