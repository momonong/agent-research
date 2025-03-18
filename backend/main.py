from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from src.clients.chat_client import init_chat_model_client
from src.agents.agent import Agent
import asyncio
import json

app = FastAPI()

client = init_chat_model_client()
system_prompt = "你是一個具有內部推理能力的助手。當你無法直接回答問題時，請啟用外部搜尋並整理資訊回答。"
agent = Agent(client, system_prompt=system_prompt, default_source=None)


async def agent_stream(query: str):
    # 使用 asyncio.to_thread 執行同步生成器
    return await asyncio.to_thread(lambda: list(agent.chat_stream(query)))

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query", "")
    if not query:
        return JSONResponse({"error": "請提供 query 參數。"}, status_code=400)
    
    return StreamingResponse(agent_stream(query), media_type="application/json")

@app.get("/")
def root():
    return {"message": "Agent API 已啟動，請使用 POST /chat 進行查詢."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)