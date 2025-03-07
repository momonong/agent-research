# src/config/app_config.py
import os
from dotenv import load_dotenv

load_dotenv()

class ModelConfig:
    def __init__(self):
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        self.AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-02-01")

class SheetConfig:
    def __init__(self):
        self.GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
        self.SHEET_NAME = "Sheet1"

class AppConfig:
    def __init__(self):
        self.model = ModelConfig()
        self.sheet = SheetConfig()

# 使用方式
config = AppConfig()
print(config.model.AZURE_OPENAI_ENDPOINT)
print(config.sheet.GOOGLE_SHEET_ID)
