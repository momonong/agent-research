from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from backend.agent_stream import agent_stream
from backend.chat_request import ChatRequest
import asyncio
import json

app = FastAPI()


# 只允許來自 localhost 的連線
@app.middleware("http")
async def ip_restriction_middleware(request: Request, call_next):
    if request.client.host not in ("127.0.0.1", "::1"):
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await call_next(request)


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    處理用戶發送的對話訊息，並返回 Agent 的回應。
    """
    query = request.query
    if not query:
        return JSONResponse({"error": "請提供 query 參數。"}, status_code=400)
    return StreamingResponse(
        agent_stream(query),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/test")
async def test_stream(request: Request):
    """
    模擬多段回覆：
    1. Chunk 1: 回傳初始的思考提示（包含 reasoning，finalized 為 False）
    2. Chunk 2: 回傳部分推理步驟（依然未完成）
    3. Chunk 3: 延遲後回傳最終答案（message）並標記 finalized 為 True
    """
    data = await request.json()
    query = data.get("query", "測試用戶訊息")

    async def fake_stream():
        # Chunk 1: 初始思考提示
        yield json.dumps(
            {"reasoning": [f"收到問題：{query}，正在思考中..."], "finalized": False}
        ) + "\n"
        await asyncio.sleep(2)

        # Chunk 2: 部分推理步驟
        yield json.dumps(
            {
                "reasoning": ["步驟1：解析問題內容", "步驟2：蒐集相關資訊"],
                "finalized": False,
            }
        ) + "\n"
        await asyncio.sleep(3)  # 延遲 3 秒，總共 5 秒後產生最終答案

        # Chunk 3: 最終答案（請注意，此處使用 "message" 欄位）
        yield json.dumps(
            {
                "text": f"最終答案：針對 '{query}' 的回答已生成。",
                "reasoning": ["步驟3：整合分析結果"],
                "finalized": True,
            }
        ) + "\n"

    return StreamingResponse(fake_stream(), media_type="ext/event-stream")


@app.get("/")
async def read_root():
    return {"message": "歡迎使用 Agent 聊天系統！請使用 POST 請求 /chat 端點。"}


if __name__ == "__main__":
    import uvicorn

    # 注意這裡根據你的資料夾結構改成 backend.main:app
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8051, reload=True)
