from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from backend.agent_stream import agent_stream
from backend.chat_request import ChatRequest
from test.fake_stream import fake_stream
import asyncio
import json
import logging

app = FastAPI()

# 設定允許的來源，這裡只允許 localhost:3000，或者你也可以使用 "*" 允許所有
origins = [
    "http://localhost:3000",
    "ming60.tplinkdns.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 或者使用 ["*"] 允許所有來源，但不推薦在生產環境
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置日誌
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 只允許來自 localhost 的連線
@app.middleware("http")
async def ip_restriction_middleware(request: Request, call_next):
    if request.client.host not in ("127.0.0.1", "::1"):
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await call_next(request)


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    處理用戶發送的對話訊息，並返回 Agent 的回應。
    """
    query = request.query
    logger.info(f"收到對話請求，query: {query}")
    
    response = StreamingResponse(agent_stream(query), media_type="application/json")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    logger.info("開始串流回應")
    return response


@app.post("/api/test")
async def test_stream(request: ChatRequest):
    """
    模擬多段回覆：
    1. Chunk 1: 回傳初始的思考提示（包含 reasoning，finalized 為 False）
    2. Chunk 2: 回傳部分推理步驟（依然未完成）
    3. Chunk 3: 延遲後回傳最終答案（message）並標記 finalized 為 True
    """
    try:
        query = request.query
        logger.info(f"收到測試請求，query: {query}")
        
        response = StreamingResponse(fake_stream(query), media_type="application/json")
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"
        
        logger.info("開始串流回應")
        return response
        
    except Exception as e:
        logger.error(f"處理測試請求時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    return {"message": "歡迎使用 Agent 聊天系統！請使用 POST 請求 /chat 端點。"}


if __name__ == "__main__":
    import uvicorn

    # 注意這裡根據你的資料夾結構改成 backend.main:app
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8051, reload=True)
