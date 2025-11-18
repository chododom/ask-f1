from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from backend.models.models import ChatRequest, ChatResponse
from backend.core.graph import agent_executor


router = APIRouter()

# In-memory storage of conversation history
memory = MemorySaver()


@router.post("/chat", response_model=ChatResponse)
async def run_workflow(question: ChatRequest):
    """Handles a single chat turn by running the agent executor."""

    input_message = [HumanMessage(content=question.query)]
    thread_id = str(question.session_id)
    config = {"configurable": {"thread_id": thread_id, "checkpointer": memory}}

    final_state = await agent_executor.ainvoke(
        {"messages": input_message}, config=config
    )

    final_response_message = final_state["messages"][-1]

    return ChatResponse(
        response=final_response_message.content, session_id=question.session_id
    )
