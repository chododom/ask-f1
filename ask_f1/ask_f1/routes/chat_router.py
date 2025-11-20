from fastapi import APIRouter

# from langchain_core.messages import HumanMessage
# from langgraph.checkpoint.memory import MemorySaver
from ask_f1.models.chat import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    ChatMessage,
)
from ask_f1.config import CFG
from ask_f1.models.models import ModelList, ModelCard
# from backend.core.graph import agent_executor


router = APIRouter()

# In-memory storage of conversation history
# memory = MemorySaver()


@router.get("/models", response_model=None)
async def list_models():
    return ModelList(
        data=[
            ModelCard(id=CFG.model_name, owned_by="me"),
        ]
    )


@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """Handles a single chat turn by running the agent executor."""
    print(request)
    return ChatCompletionResponse(
        choices=[
            ChatCompletionChoice(
                index=0,
                message=ChatMessage(role="assistant", content="Zdravicko"),
                finish_reason="stop",
            )
        ]
    )
