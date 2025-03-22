from src.clients.model_client import init_model_client
from src.agents.agent import Agent
import logging
import asyncio
import json

logger = logging.getLogger(__name__)

client = init_model_client()
agent = Agent(client, default_source=None)


async def agent_stream(query: str):
    """
    將 OpenAI 回應轉換為前端期望的格式
    """
    try:
        logger.info(f"開始處理 agent_stream 請求，query: {query}")

        async for msg in agent.chat_stream(query):
            logger.debug("收到原始回應: %s", msg)

            # 轉換格式
            if msg.get("message") is None:
                response_data = {
                    "reasoning": msg.get("reasoning", []),
                    "finalized": msg.get("finalized"),
                }
            else:
                response_data = {
                    "message": msg.get("message", ""),
                    "finalized": msg.get("finalized"),
                    "reasoning": msg.get("reasoning"),
                }

            logger.debug("轉換後的回應: %s", response_data)
            yield json.dumps(response_data, ensure_ascii=False) + "\n"
            await asyncio.sleep(0.1)

        logger.info("完成 agent_stream 請求處理")

    except Exception as e:
        logger.error(f"agent_stream 處理過程中發生錯誤: {str(e)}")
        yield json.dumps(
            {"error": f"處理請求時發生錯誤: {str(e)}", "finalized": True},
            ensure_ascii=False,
        ) + "\n"
