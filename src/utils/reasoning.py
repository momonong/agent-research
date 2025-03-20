def generate_reasoning(query, client):
    """
    利用模型生成推理過程，要求模型用 <step1>, <step2>, ... 來分隔各步驟。
    參數：
        - query: 用戶查詢
        - client: 用於呼叫模型的客戶端
    返回：
        - 模型生成的原始推理過程文本
    """
    prompt = (
        f'''
        請詳細描述你如何思考下面這個問題的推理過程，
        並用 <step1>, <step2>, <step3> 等標記分隔每個步驟。\n
        問題：{query}\n推理過程：
        '''
    )
    messages = [{"role": "system", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
    )
    reasoning_text = response.choices[0].message.content.strip()
    return reasoning_text

def parse_reasoning_text(raw_ct: str) -> list:
    """
    根據分隔符號解析原始推理過程文本，返回步驟列表。
    假設每個步驟以 "<step" 為開頭。
    """
    steps = []
    if "<step" in raw_ct:
        parts = raw_ct.split("<step")
        for part in parts[1:]:
            step = "<step" + part.strip()
            steps.append(step)
    else:
        steps.append(raw_ct)
    return steps

def format_reasoning_text(chain: list) -> str:
    """
    將推理過程列表轉換為一個公開的摘要，用於前端展示。
    這裡可以做簡單的連接，也可以進一步過濾不適合公開的細節。
    """
    # 此示例簡單地以 " -> " 連接所有步驟
    return " -> ".join(chain)
