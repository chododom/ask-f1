from backend.config.config import CFG

# from langchain_ollama import ChatOllama
from langchain_google_vertexai import ChatVertexAI


# llm = ChatOllama(
#     model=CFG.model_name,
#     temperature=CFG.temperature,
#     base_url="http://localhost:11434"
# )

llm = ChatVertexAI(
    model=CFG.model_name,
    temperature=CFG.temperature,
)
