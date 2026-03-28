import logging

def append_with_duplicate_check(existing_steps: list, new_step: str) -> bool:
    """
    檢查並將新的步驟 new_step 追加到 existing_steps 列表中。
    如果 new_step 已經存在，則記錄重複 log；無論是否重複，都會追加到列表中（後續可調整）。
    
    參數:
        existing_steps (list): 目前的推理步驟列表。
        new_step (str): 新的步驟內容。
    
    返回:
        bool: 如果 new_step 已存在，則返回 True；否則返回 False。
    """
    # 移除左右空白
    new_step = new_step.strip()
    if not new_step:
        logging.debug("忽略空的推理步驟")
        return False

    if new_step in existing_steps:
        logging.debug("檢測到重複推理步驟: %s", new_step)
        # 目前仍將重複的步驟追加到列表中，你可以根據需要決定是否要跳過這一步
        existing_steps.append(new_step)
        return True
    else:
        logging.debug("新增推理步驟: %s", new_step)
        existing_steps.append(new_step)
        return False

def append_unique(steps: list, new_step: str) -> bool:
    """
    將 new_step 追加到 steps 中，如果 steps 已經包含相同內容則不追加。
    
    參數:
        steps (list): 已存在的步驟列表。
        new_step (str): 要追加的新步驟。
    
    返回:
        bool: 如果步驟已經存在則返回 True，否則返回 False（表示成功追加）。
    """
    # 清理左右空白
    new_step = new_step.strip()
    if not new_step:
        logging.debug("忽略空的步驟")
        return False

    if new_step in steps:
        logging.debug("重複步驟，跳過追加：%s", new_step)
        return True
    else:
        steps.append(new_step)
        logging.debug("追加新步驟：%s", new_step)
        return False