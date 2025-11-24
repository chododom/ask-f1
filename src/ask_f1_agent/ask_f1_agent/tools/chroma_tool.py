from typing import Any, Dict, List

from langchain.tools import tool
from langchain_core.documents import Document
from pydantic import BaseModel, Field

from ask_f1_agent.services.chroma_db import get_chroma_retriever
from ask_f1_agent.utils.logger import logger


class DocumentSearchInput(BaseModel):
    search_phrase: str = Field(
        ...,
        description="A highly specific, refined, and extracted key phrase from the user's message. \
            The search phrase should be formatted to perform a precise similarity search \
            against the FIA F1 sporting regulation documents. For example, if the user asks 'What is the rule about overtaking under a safety car?', \
            the input MUST be: 'overtaking under a safety car' (do not include the title of the document, or any extraneous text).",
    )


# @traceable(run_type="tool", name="F1 Regulations Search")
@tool("document_search", args_schema=DocumentSearchInput)
def document_search(search_phrase: str) -> List[Dict[str, Any]]:
    """
    Searches the official FIA F1 sporting regulations for documents relevant
    to the input search phrase. Use this tool only for questions about the sporting regulations and rules.

    Returns:
        A list of dictionaries, where each dictionary contains the 'page_content'
        and 'metadata' of the retrieved documents.
    """
    logger.debug(f"Document Search Tool invoked with search phrase: {search_phrase}")

    try:
        chroma_retriever = get_chroma_retriever()
    except RuntimeError as e:
        logger.error(f"ChromaDBService not initialized: {e}")
        return []

    try:
        retrieved_docs: List[Document] = chroma_retriever.invoke(search_phrase)
    except Exception as e:
        logger.error(f"Error during document retrieval: {e}")
        return []

    if not retrieved_docs:
        logger.debug("Document Search Tool found no relevant documents.")
        return []

    logger.debug(f"Document Search Tool retrieved {len(retrieved_docs)} documents.")
    try:
        formatted_results = [{"content": doc.page_content, "metadata": doc.metadata} for doc in retrieved_docs]
    except Exception as e:
        logger.error(f"🛠️ Error formatting retrieved documents: {e}")
        return []

    logger.debug(f"🛠️ Document Search Tool finished with response: {formatted_results}")
    return formatted_results
