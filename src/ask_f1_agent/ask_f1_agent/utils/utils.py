import importlib
import importlib.metadata

from pathlib import Path
from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ask_f1_agent.models.chat import ChatMessage


def get_package_root(package_name: str) -> Path:
    """Get the root directory of a given package."""
    root = importlib.resources.files(package_name)
    assert isinstance(root, Path), f"Expected Path, got {type(root)}"
    return root


def get_version() -> str:
    return importlib.metadata.version(__package__ or __name__)


def openapi_to_langchain_messages(messages: List[ChatMessage]):
    lc_messages = []
    for msg in messages:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))
        elif msg.role == "system":
            lc_messages.append(SystemMessage(content=msg.content))

    return lc_messages
