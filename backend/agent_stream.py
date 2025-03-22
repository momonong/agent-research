from src.clients.model_client import init_model_client
from src.agents.agent import Agent
import asyncio
import json


client = init_model_client()
agent = Agent(client, default_source=None)


async def agent_stream(query):
    """
    將 agent.chat_stream 的同步生成器包裝為非同步生成器，
    逐步傳送每個訊息給前端，並以 JSON 格式的字串換行分隔。
    """
    async for msg in agent.chat_stream(query):
        yield json.dumps(msg) + "\n"
        await asyncio.sleep(0.1)


