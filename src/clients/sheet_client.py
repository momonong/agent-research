import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.config import SheetConfig

config = SheetConfig()

def init_google_sheet():
    """
    使用 Service Account 讀取指定 Google Sheet 的內容。
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    # 請將你的憑證放在專門的資料夾中，並在 .gitignore 中忽略
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "keys/sylvan-journey-452010-m8-cfee3a5341c5.json", scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(config.GOOGLE_SHEET_ID).worksheet(config.SHEET_NAME)
    return sheet

if __name__ == "__main__":
    sheet = init_google_sheet()
    print("Google Sheet client initialized.")
