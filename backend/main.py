from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from src.clients.model_client import init_model_client
from src.agents.agent import Agent
from backend.chat_request import ChatRequest
import asyncio
import json

app = FastAPI()

client = init_model_client()
agent = Agent(client, default_source=None)


async def agent_stream(query):
    """
    將 agent.chat_stream 的同步生成器包裝為非同步生成器，
    逐步傳送每個訊息給前端，並以 JSON 格式的字串換行分隔。
    """
    # 利用 asyncio.to_thread 執行同步生成器，收集所有訊息
    messages = await asyncio.to_thread(lambda: list(agent.chat_stream(query)))
    for msg in messages:
        # 將每個訊息轉換成 JSON 字串後 yield 出來
        yield json.dumps(msg) + "\n"
        await asyncio.sleep(0.1)


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    處理用戶發送的對話訊息，並返回 Agent 的回應。
    """
    query = request.query
    if not query:
        return JSONResponse({"error": "請提供 query 參數。"}, status_code=400)
    return StreamingResponse(agent_stream(query), media_type="application/json")


@app.get("/test")
async def test_stream():
    async def fake_stream():
        # 模擬幾個步驟的訊息
        simulated_messages = [
            {"role": "user", "content": "測試用戶訊息"},
            {"role": "system", "content": "Step 1: 收到使用者輸入。"},
            {"role": "system", "content": "Step 2: 正在處理請求..."},
            {"role": "assistant", "content": "這是中間回覆..."},
            {
                "role": "assistant",
                "content": "最終答案：這是最終回覆。",
                "finalized": True,
            },
        ]
        for msg in simulated_messages:
            # 將每個訊息轉成 JSON 字串並換行分隔
            yield json.dumps(msg) + "\n"
            await asyncio.sleep(0.5)  # 模擬延遲

    return StreamingResponse(fake_stream(), media_type="application/json")


@app.get("/")
async def read_root():
    return {"message": "歡迎使用 Agent 聊天系統！請使用 POST 請求 /chat 端點。"}


if __name__ == "__main__":
    import uvicorn

    # 注意這裡根據你的資料夾結構改成 backend.main:app
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8051, reload=True)
