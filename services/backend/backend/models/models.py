from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class ChatRequest(BaseModel):
    """Model for an incoming chat message."""

    query: str = Field(..., description="The user's message.")
    session_id: UUID = Field(
        default_factory=uuid4,
        description="Unique session identifier for the conversation.",
    )


class ChatResponse(BaseModel):
    """Model for an outgoing chat response."""

    response: str = Field(..., description="The final text response from the agent.")
    session_id: UUID = Field(
        ..., description="Unique session identifier for the conversation."
    )
