from rapidfuzz import fuzz
from dotenv import load_dotenv
from src.config import init_google_sheet

load_dotenv()


def load_google_sheet():
    """
    從 Google Sheet 載入常見問答資料。
    """
    sheet = init_google_sheet()
    data = sheet.get_all_records()
    return data


def get_preferred_answer(query, google_sheet, threshold=40):
    """
    根據 query 在 preferred_answers 中進行模糊匹配，返回最合適的預設回答。

    :param query: 使用者輸入的問題文字
    :param google_sheet: 從 Google Sheet 載入的字典列表，每筆記錄應包含 "問題" 與 "AI回覆"
    :param threshold: 相似度門檻（0-100），超過此門檻則認為匹配
    :return: 如果有匹配，返回對應的 "AI回覆"，否則返回 None
    """
    # 使用 rapidfuzz 模組計算相似度
    best_match = None
    best_score = 0

    for record in google_sheet:
        candidate = record.get("問題", "")
        score = fuzz.token_set_ratio(query, candidate)
        if score > best_score:
            best_score = score
            best_match = record
    # default threshold = 40
    if best_score >= threshold:
        print("最佳匹配：", best_match.get("問題", ""))
        print("相似度：", best_score)
        return best_match.get("回覆有誤", None)
    return None


if __name__ == "__main__":
    answers = load_google_sheet()
    print("從 Google Sheet 載入的預設回答資料：")
    for record in answers:
        print(record)

    # 測試模糊匹配
    test_query = "申請復學的居留簽證的時候需要的復學證明可以什麼時候拿到?"
    matched_answer = get_preferred_answer(test_query, answers)
    print("\n對於查詢：", test_query)
    print("匹配到的預設回答：", matched_answer)
