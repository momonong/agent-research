import asyncio
import json
import logging

# 配置日誌
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fake_stream(query: str):
    logger.info(f"開始處理查詢: '{query}'")
    
    # Chunk 0: 初始思考提示
    logger.debug("生成初始思考提示")
    yield json.dumps({
        "reasoning": [f"收到問題：{query}，正在思考中...\n**開始分析**"],
        "finalized": False
    }) + "\n"
    await asyncio.sleep(2)
    logger.debug("初始思考提示已生成")
    
    # Chunk 1: 部分推理步驟
    logger.debug("生成部分推理步驟1")
    yield json.dumps({
        "reasoning": [
            "### 步驟1：資料分析\n\n" +
            "| 分析項目 | 狀態 | 說明 |\n" +
            "|----------|------|------|\n" +
            "| 數據清理 | ✅ | 已完成初步處理 |\n" +
            "| 格式驗證 | ⏳ | 進行中 |\n" +
            "| 異常檢測 | 🔄 | 待處理 |\n\n" +
            "#### 待辦事項：\n\n" +
            "- [x] 導入原始數據\n" +
            "- [ ] 執行數據轉換\n" +
            "- [ ] 生成分析報告"
        ],
        "finalized": False
    }) + "\n"
    await asyncio.sleep(3)
    logger.debug("部分推理步驟1已生成")
    
    # Chunk 2: 部分推理步驟
    logger.debug("生成部分推理步驟2")
    yield json.dumps({
        "reasoning": [
            "### 步驟2：技術細節\n\n" +
            "> 💡 **重要提示**\n" +
            "> 以下是核心處理邏輯：\n\n" +
            "```python\n" +
            "def process_data(data):\n" +
            "    return {\n" +
            "        'status': 'success',\n" +
            "        'metrics': {\n" +
            "            'accuracy': 0.95,\n" +
            "            'recall': 0.89\n" +
            "        }\n" +
            "    }\n" +
            "```\n\n" +
            "#### 性能指標\n\n" +
            "| 指標 | 數值 | 目標 |\n" +
            "|------|------|------|\n" +
            "| 準確率 | 95% | 90% |\n" +
            "| 召回率 | 89% | 85% |\n" +
            "| 處理時間 | 1.2s | 2.0s |"
        ],
        "finalized": False
    }) + "\n"
    logger.debug("部分推理步驟2已生成")

    # Chunk 3: 最終答案
    logger.debug("生成最終答案")
    yield json.dumps({
        "message": (
            "# 分析報告\n\n" +
            f"## 查詢：'{query}'\n\n" +
            "### 主要發現\n\n" +
            "| 類別 | 結果 | 可信度 |\n" +
            "|------|------|--------|\n" +
            "| 類型A | 正面 | 高 |\n" +
            "| 類型B | 中性 | 中 |\n" +
            "| 類型C | 待定 | 低 |\n\n" +
            "### 詳細說明\n\n" +
            "> 📊 **數據摘要**\n" +
            "> - 樣本數量：1000\n" +
            "> - 處理時間：1.2秒\n" +
            "> - 準確度：95%\n\n" +
            "#### 技術細節\n\n" +
            "```json\n" +
            "{\n" +
            "    \"status\": \"success\",\n" +
            "    \"version\": \"1.0.0\",\n" +
            "    \"timestamp\": \"2024-03-21\"\n" +
            "}\n" +
            "```"
        ),
        "reasoning": [
            "### 步驟3：最終總結\n\n" +
            "- ✅ 數據分析完成\n" +
            "- 📈 性能達標\n" +
            "- 📋 報告生成"
        ],
        "finalized": True
    }) + "\n"
    logger.info(f"查詢 '{query}' 處理完成")

    return # 結束生成器