from src.clients.model_client import init_model_client


def get_raw_info(info: dict) -> str:
    """
    將提供的資訊進行摘要整理，返回綜合答案。

    參數：
        - info: 一個字典，包含需要整合的資訊。
            例如：{"raw_search_results": [...], "chain_of_thought": [...]}
        - context: 其他附加上下文，用來指導摘要的重點。

    回傳：
        - 模型生成的綜合答案。
    """
    # 將所有資訊整合成一個長文本
    raw_info = "查詢結果：\n"

    # 網路搜尋結果
    if "raw_search_results" in info:
        for item in info.get("raw_search_results", []):
            raw_info += f"- {item.get('title', '')} ({item.get('link', '')})\n"
        raw_info += "\n思考過程：\n" + "\n".join(info.get("reasoning", [])) + "\n"

    # 時間推理結果
    if "current_time" in info:
        raw_info += "當前時間：\n" + info.get("current_time", "") + "\n"
        raw_info += "\n思考過程：\n" + "\n".join(info.get("reasoning", [])) + "\n"

    return raw_info


def summarize_result(info: dict) -> str:
    """
    將提供的資訊進行摘要整理，返回綜合答案。

    參數：
        - info: 一個字典，包含需要整合的資訊。
            例如：{"raw_search_results": [...], "chain_of_thought": [...]}
        - context: 其他附加上下文，用來指導摘要的重點。

    回傳：
        - 模型生成的綜合答案。
    """
    raw_info = get_raw_info(info)

    prompt = (
        "請根據以下資訊，列出與查詢最相關的具體資訊和細節，"
        "是收到的資訊長度及複雜度而定"
        "若簡單的資訊則直接回答，"
        "若複雜的資訊則先以摘要的形式統整回答，"
        "再以列點的方式進行補充：\n\n"
        f"{raw_info}\n\n"
        "最終回答："
    )

    client = init_model_client()
    messages = [
        {"role": "system", "content": "你是一個專業的資訊統整助手。"},
        {"role": "user", "content": prompt},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"摘要生成出錯：{e}"

