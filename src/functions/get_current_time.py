from datetime import datetime

def get_current_time() -> str:
    """
    返回當前系統時間，格式為 "YYYY-MM-DD HH:MM:SS"。
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")