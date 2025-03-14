# src/config/app_config.py
import os
from dotenv import load_dotenv

load_dotenv()

class ChatModelConfig:
    def __init__(self):
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        self.AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-02-01")

class SheetConfig:
    def __init__(self):
        self.GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
        self.SHEET_NAME = "Sheet1"

class ScraperModelConfig:
    def __init__(self):
        # 模型相關設定：AzureOpenAI
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        self.API_VERSION = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
        self.AZURE_DEPLOYMENT = "gpt-4o"   # 請根據你的部署名稱修改
        self.TOP_P = 1
        self.PRESENCE_PENALTY= 2
        self.TEMPERATURE = 0
        self.MAX_TOKENS = 3500
        self.MODEL_TOKENS = 100000

class ScraperEmbeddingConfig:
    def __init__(self):
        # 嵌入模型相關設定：OpenAIEmbeddings
        self.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        self.API_VERSION = os.getenv("OPENAI_EMBEDDINGS_VERSION", "2023-05-15")
        self.AZURE_EMBEDDING_DEPLOYMENT = "text-embedding-3-large"
        self.AZURE_ENDPOINT_EMBEDDINGS = os.getenv("AZURE_ENDPOINT_EMBEDDINGS")
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

class ScraperConfig:
    def __init__(self):
        self.model = ScraperModelConfig()
        self.embeddings = ScraperEmbeddingConfig()

class AppConfig:
    def __init__(self):
        self.chat_model = ChatModelConfig()
        self.sheet = SheetConfig()
        self.scraper = ScraperConfig()

if __name__ == "__main__":
    app_config = AppConfig()
    print("App config initialized.")