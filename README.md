# AI 智慧助手系統

這是一個基於 FastAPI 和 Azure OpenAI 服務打造的智慧對話系統，具備網路搜索、網頁爬蟲、資料庫查詢等多項功能。

## 功能特點

- 🤖 智慧對話：使用 GPT-4 模型進行自然語言對話
- 🔍 網路搜索：可以即時搜索網路資訊並整合回答
- 🕷️ 智能爬蟲：支援網頁內容抓取和分析
- 📊 Google Sheet 整合：支援從試算表讀取預設答案
- ⏰ 即時資訊：具備獲取當前時間等即時資訊功能
- 🔄 串流回應：支援對話內容串流輸出
- 🧠 推理過程：展示 AI 的思考和推理步驟

## 系統架構

``` shell
project/
├── backend/ # 後端服務
│ ├── main.py # FastAPI 主程序
│ └── chat_request.py # 請求模型定義
├── src/
│ ├── agents/ # AI 代理邏輯
│ ├── clients/ # 各類客戶端
│ ├── functions/ # 功能模組
│ ├── tools/ # 工具類
│ └── config.py # 配置文件
```


## 環境設定

1. 建立 `.env` 檔案並設定以下環境變數：
   ``` .env
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_API_VERSION=2024-02-01
   GOOGLE_SHEET_ID=your_sheet_id
   ```

2. 安裝相依套件：
   ``` shell
   pip install -r requirements.txt
   ```

## 使用方式

### 啟動後端服務
``` shell
python -m backend.main
```

服務將在 `http://localhost:8051` 啟動

### API 端點

- `GET /`: 歡迎頁面
- `POST /chat`: 對話端點
  - Request Body:
    ```json
    {
        "query": "你的問題"
    }
    ```
  - Response: 串流形式的 JSON 回應

### 命令列介面

也可以直接使用命令列介面進行測試：
``` bash
python -m src.main
```

## 核心功能模組

- `Agent`: 智慧代理，負責對話管理和功能調用
- `web_search`: 網路搜索功能
- `scraper`: 網頁爬蟲功能
- `summarize_result`: 結果摘要整理
- `preferred_answers`: Google Sheet 預設答案查詢

## 開發說明

- 使用 FastAPI 框架開發 RESTful API
- 採用 Azure OpenAI 服務作為底層模型
- 支援非同步串流響應
- 模組化設計，易於擴展

## 注意事項

- 需要有效的 Azure OpenAI API 金鑰
- 使用前請確保網路連接正常
- 建議在虛擬環境中運行專案
