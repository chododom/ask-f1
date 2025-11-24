from fastapi import APIRouter, HTTPException

from ask_f1_agent.agent.graph import agent_executor
from ask_f1_agent.config import CFG
from ask_f1_agent.models.chat import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
)
from ask_f1_agent.models.models import ModelCard, ModelList
from ask_f1_agent.utils.utils import openapi_to_langchain_messages

router = APIRouter()


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

    if not agent_executor:
        raise RuntimeError("Agent graph not initialized")

    messages = openapi_to_langchain_messages(request.messages)

    # Run the graph
    try:
        final_state = await agent_executor.ainvoke(
            {"messages": messages}, config={"recursion_limit": 15, "thread_id": "1"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Extract response
    last_message = final_state["messages"][-1]
    content = last_message.content if isinstance(last_message.content, str) else str(last_message.content)

    return ChatCompletionResponse(
        choices=[
            ChatCompletionChoice(
                index=0,
                message=ChatMessage(role="assistant", content=content),
                finish_reason="stop",
            )
        ]
    )
