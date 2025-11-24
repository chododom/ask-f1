from pydantic_settings import BaseSettings, SettingsConfigDict

from ask_f1_agent.utils.logger import logger


class Config(BaseSettings):
    package_name: str = "ask_f1_agent"
    log_level: str = "INFO"

    # LLM settings
    model_name: str = "gemini-2.5-flash"
    # llm_endpoint_url: str = 'http://localhost:8000/v1'
    temperature: float = 0.0

    sys_prompt_path: str = "prompts/system_prompt.txt"

    # ChromaDB settings
    chroma_persistence_dir: str = "chroma_db"  # in relation to ask_f1_agent root
    chroma_collection_name: str = "rag_documents"

    mcp_url: str = "http://localhost:8000/mcp"

    model_config = SettingsConfigDict(env_file=".env")


CFG = Config()

logger.setLevel(CFG.log_level)
logger.info(f"Config: {CFG}")
