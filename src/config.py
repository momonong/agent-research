import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def init_openai_client():
    """
    載入環境變數並初始化 AzureOpenAI 客戶端。
    """
    load_dotenv()
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
    )
    return client

if __name__ == '__main__':
    client = init_openai_client()
    print("AzureOpenAI client initialized.")
