def build_function_prompt(functions: list) -> str:
    """
    根據 function definitions 動態生成描述文字，
    每個 function 包含其名稱和描述，並換行排列。
    """
    lines = []
    for func in functions:
        name = func.get("name", "")
        desc = func.get("description", "")
        line = f"{name}: {desc}"
        lines.append(line)
    return "\n".join(lines)


def generate_reasoning(client, query, functions=None):
    """
    利用模型生成推理過程，要求模型用 <step1>, <step2>, ... 來分隔各步驟。
    參數：
        - query: 用戶查詢
        - client: 用於呼叫模型的客戶端
    返回：
        - 模型生成的原始推理過程文本
    """
    func_info = build_function_prompt(functions)
    prompt = f"""
        請詳細描述你如何思考下面這個問題的推理過程，
        並且考慮到你可以調用以下外部功能來獲取最新資訊：\n
        {func_info}\n\n
        並用 <step1>, <step2>, <step3> 等標記分隔每個步驟。\n
        問題：{query}\n推理過程：
        """
    messages = [{"role": "system", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
    )
    reasoning_text = response.choices[0].message.content.strip()
    return reasoning_text


def parse_reasoning_text(raw_reasoning: str) -> list:
    """
    根據分隔符號解析原始推理過程文本，返回步驟列表。
    假設每個步驟以 "<step" 為開頭。
    """
    steps = []
    # print(f'\nraw_reasoning:\n{raw_reasoning}')
    if "<step" in raw_reasoning:
        parts = raw_reasoning.split("<step")
        for part in parts[1:]:
            step = "<step" + part.strip()
            steps.append(step)
    else:
        steps.append(raw_reasoning)
    return steps


def generate_final_answer(client, query: str, steps: str) -> str:
    """
    將完整的推理過程作為上下文生成最終答案。
    """
    prompt = f"""
        根據以下推理過程，請給出問題「{query}」的最終答案：\n
        {steps}\n
        最終答案：
    """
    messages = [{"role": "system", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
    )
    answer = response.choices[0].message.content.strip()
    return answer
