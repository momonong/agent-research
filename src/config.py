import os
import gspread
from dotenv import load_dotenv
from openai import AzureOpenAI
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()


def init_openai_client():
    """
    載入環境變數並初始化 AzureOpenAI 客戶端。
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
    )
    return client


def init_google_sheet():
    """
    使用 Service Account 讀取指定 Google Sheet 的內容。
    """
    # 定義 Google Sheet ID 和工作表名稱
    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheet_name = "Sheet1"

    # 定義 API 存取範圍
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    # 載入 Service Account 憑證
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "sylvan-journey-452010-m8-cfee3a5341c5.json", scope
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    return sheet


if __name__ == "__main__":
    client = init_openai_client()
    print("AzureOpenAI client initialized.")
