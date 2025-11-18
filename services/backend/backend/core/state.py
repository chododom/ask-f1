from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from operator import add  # Used as the reducer function


class AgentState(TypedDict):
    """
    Represents the state of our LangGraph agent.

    This state is passed around the graph and updated by the nodes.
    """

    messages: Annotated[List[BaseMessage], add]  # Conversation History
