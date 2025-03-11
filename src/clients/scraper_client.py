import warnings
from src.config import ScraperConfig
from langchain_openai import AzureChatOpenAI, OpenAIEmbeddings

warnings.filterwarnings(
    "ignore",
    message=r"WARNING! (azure_endpoint|model_instance|model_tokens) is not default parameter\.",
)

config = ScraperConfig()


def init_scraper_config() -> dict:
    """
    使用配置初始化 AzureChatOpenAI 與 OpenAIEmbeddings，返回一個 scraper_config 字典。
    """
    # 初始化 AzureChatOpenAI 模型實例
    llm_model_instance = AzureChatOpenAI(
        api_version=config.model.API_VERSION,
        top_p=config.model.TOP_P,
        presence_penalty=config.model.PRESENCE_PENALTY,
        azure_deployment=config.model.AZURE_DEPLOYMENT,
        azure_endpoint=config.model.AZURE_OPENAI_ENDPOINT,
        temperature=config.model.TEMPERATURE,
        max_tokens=config.model.MAX_TOKENS,
        api_key=config.model.AZURE_OPENAI_API_KEY,
    )

    # 初始化 OpenAIEmbeddings 模型實例
    embedder_model_instance = OpenAIEmbeddings(
        openai_api_key=config.embeddings.AZURE_OPENAI_API_KEY,
        openai_api_version=config.embeddings.API_VERSION,
        deployment=config.embeddings.AZURE_EMBEDDING_DEPLOYMENT,
        azure_endpoint=config.embeddings.AZURE_OPENAI_ENDPOINT,
    )

    scraper_config = {
        "llm": {
            "model_instance": llm_model_instance,
            "model_tokens": config.model.MODEL_TOKENS,
        },
        "embeddings": {
            "model_instance": embedder_model_instance,
        },
    }
    return scraper_config


if __name__ == "__main__":
    scraper = init_scraper_config()
    print("Scraper config initialized.")
