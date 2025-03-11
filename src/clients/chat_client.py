from openai import AzureOpenAI
from src.config import ChatModelConfig

config = ChatModelConfig()


def init_chat_model_client():
    """
    使用 config 中的參數初始化 AzureOpenAI 客戶端，
    未來如果需要支持其他模型供應商，可在此處擴展。
    """
    client = AzureOpenAI(
        azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        api_key=config.AZURE_OPENAI_API_KEY,
        api_version=config.AZURE_API_VERSION,
    )
    return client


if __name__ == "__main__":
    client = init_chat_model_client()
    print("Model client initialized.")
