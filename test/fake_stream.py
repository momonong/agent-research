import asyncio
import json
import logging

# 配置日誌
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def fake_stream(query: str):
    logger.info(f"開始處理查詢: '{query}'")
    
    # Chunk 0: 初始思考提示 (Step 1)
    logger.debug("生成初始思考提示")
    yield json.dumps({
        "reasoning": [
            f"<step1> 收到問題：{query}，正在開始分析。這是初始階段，我正在整理思路以便後續處理。"
        ],
        "finalized": False
    }, ensure_ascii=False) + "\n"
    await asyncio.sleep(2)
    logger.debug("初始思考提示已生成")
    
    # Chunk 1: 部分推理步驟1 (Step 2)
    logger.debug("生成部分推理步驟1")
    yield json.dumps({
        "reasoning": [
            "<step2> ### 步驟1：資料分析\n\n" +
            "在這一步中，我會先檢查並整理與查詢相關的資料。這包括從內部資料庫抽取關鍵字、清洗數據以及確定哪些資訊是最有價值的。 \n\n" +
            "詳細步驟如下：\n" +
            "- **數據清理**：剔除無關或重複數據，確保數據的準確性。\n" +
            "- **格式驗證**：檢查資料格式是否符合預期，對格式不符的資料進行修正。\n" +
            "- **異常檢測**：識別並標記可能的異常數據，以便進一步處理。\n\n" +
            "待辦事項：\n" +
            "- [x] 導入原始數據\n" +
            "- [ ] 執行數據轉換\n" +
            "- [ ] 生成初步分析報告"
        ],
        "finalized": False
    }, ensure_ascii=False) + "\n"
    await asyncio.sleep(3)
    logger.debug("部分推理步驟1已生成")
    
    # Chunk 2: 部分推理步驟2 (Step 3)
    logger.debug("生成部分推理步驟2")
    yield json.dumps({
        "reasoning": [
            "<step3> ### 步驟2：技術細節與方法說明\n\n" +
            "在這一步中，我將介紹核心的技術細節和處理邏輯。這些技術細節幫助我確定數據處理的方向，並保障最終結果的準確性。 \n\n" +
            "具體說明如下：\n" +
            "> 💡 **重要提示**：下面展示了我處理資料的主要方法，並給出部分示例代碼以便參考。\n\n" +
            "```python\n" +
            "def process_data(data):\n" +
            "    # 此處執行數據處理邏輯\n" +
            "    cleaned_data = clean_data(data)\n" +
            "    validated_data = validate_format(cleaned_data)\n" +
            "    result = analyze(validated_data)\n" +
            "    return result\n" +
            "```\n\n" +
            "此外，我還會計算關鍵性能指標，如準確率、召回率及處理時間：\n\n" +
            "| 指標     | 數值 | 目標  |\n" +
            "|----------|------|-------|\n" +
            "| 準確率   | 95%  | 90%   |\n" +
            "| 召回率   | 89%  | 85%   |\n" +
            "| 處理時間 | 1.2s | 2.0s  |"
        ],
        "finalized": False
    }, ensure_ascii=False) + "\n"
    logger.debug("部分推理步驟2已生成")

    # Chunk 3: 最終答案 (Step 4)
    logger.debug("生成最終答案")
    yield json.dumps({
        "message": (
            "<step4> # 分析報告與結論\n\n" +
            f"## 查詢：'{query}'\n\n" +
            "經過上述步驟的數據分析和技術處理，以下是我對查詢的總結結果：\n\n" +
            "### 主要發現\n\n" +
            "| 類別   | 結果   | 可信度 |\n" +
            "|--------|--------|--------|\n" +
            "| 類型A  | 正面   | 高     |\n" +
            "| 類型B  | 中性   | 中     |\n" +
            "| 類型C  | 待定   | 低     |\n\n" +
            "### 詳細說明\n\n" +
            "數據分析表明，查詢結果中大部分資訊都符合預期，並且性能指標達到了既定目標。技術細節部分也展示了整體處理流程和結果的可靠性。\n\n" +
            "#### 技術細節摘要\n\n" +
            "```json\n" +
            "{\n" +
            '    "status": "success",\n' +
            '    "version": "1.0.0",\n' +
            '    "timestamp": "2024-03-21"\n' +
            "}\n" +
            "```\n\n" +
            "如果需要更深入的分析或進一步的數據解讀，請告知！"
        ),
        "reasoning": [
            "<step4> ### 步驟3：最終總結與報告生成\n\n" +
            "- 數據分析已完成，性能達標。\n" +
            "- 核心處理邏輯及技術細節清晰。\n" +
            "- 報告生成並整合了所有分析結果。"
        ],
        "finalized": True
    }, ensure_ascii=False) + "\n"
    logger.info(f"查詢 '{query}' 處理完成")
    
    return  # 結束生成器

# 測試使用（需要在 async 環境中運行）
# async def main():
#     async for chunk in fake_stream("測試查詢"):
#         print(chunk)
#
# asyncio.run(main())
