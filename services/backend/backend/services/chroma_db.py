import chromadb
from langchain_community.embeddings import SentenceTransformerEmbeddings
from backend.config.config import CFG
from backend.utils.logger import logger
from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever


# Global variable to hold the initialized service instance (initialized in FastAPI lifespan on startup)
CHROMA_SERVICE_INSTANCE = None


class ChromaDBService:
    def __init__(self, persist_directory: Path = None):
        self.client = chromadb.PersistentClient(
            settings=chromadb.Settings(
                persist_directory=str(persist_directory),
            )
        )

        # Initialize embedding function (same as used in ingest.py)
        self.embedding_function = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # Get or create the default collection where vectors will be stored
        self.collection = self.client.get_or_create_collection(
            name=CFG.chroma_collection_name,
        )

    def get_client(self):
        return self.client

    def get_embedding_function(self):
        return self.embedding_function

    def close(self):
        try:
            self.client.persist()  # uses SQLite to persist data to disk
        except Exception as e:
            logger.error(f"Error persisting ChromaDB client: {e}")


def get_chroma_retriever() -> VectorStoreRetriever:
    global CHROMA_SERVICE_INSTANCE
    if CHROMA_SERVICE_INSTANCE is None:
        raise RuntimeError(
            "ChromaDBService is not initialized. Run the lifespan event first."
        )

    chroma_store = Chroma(
        client=CHROMA_SERVICE_INSTANCE.get_client(),
        collection_name=CFG.chroma_collection_name,
        embedding_function=CHROMA_SERVICE_INSTANCE.get_embedding_function(),
    )

    retriever = chroma_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    )

    return retriever
