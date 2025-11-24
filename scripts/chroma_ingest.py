import os
import shutil
from pathlib import Path
from typing import List

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings


# --- Configuration ---
DATA_PATH = Path("data")
CHROMA_PATH = DATA_PATH / "chroma_db"
COLLECTION_NAME = "rag_documents"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_documents() -> List[Document]:
    """Loads all PDF documents from the specified data directory."""
    if not DATA_PATH.exists():
        print(f"Directory '{DATA_PATH}' does not exist. Creating it.")
        DATA_PATH.mkdir()
        print(
            f"Please place your source documents (e.g., F1_Regulations.pdf) in the created folder."
        )
        return []

    pdf_loader = DirectoryLoader(
        DATA_PATH.as_posix(),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        silent_errors=True,
    )

    print(f"Loading documents from {DATA_PATH}...")
    documents = pdf_loader.load()
    print(f"Loaded {len(documents)} source documents.")
    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """Splits documents into smaller, manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len
    )
    print(
        f"Splitting documents into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})..."
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    return chunks


def save_to_chroma(chunks: List[Document]):
    """Embeds and stores the document chunks in ChromaDB."""

    if not chunks:
        print("No chunks to process. Exiting ingestion.")
        return

    # Initialize the embedding model (MUST be the same one used by the retriever!)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Optional: Delete existing database files to ensure a clean re-ingestion
    if os.path.exists(CHROMA_PATH):
        print(f"Removing existing database at {CHROMA_PATH}...")
        shutil.rmtree(CHROMA_PATH)

    # Create a new ChromaDB instance from the documents
    print(f"Creating new ChromaDB instance and saving to disk at {CHROMA_PATH}...")
    db = Chroma.from_documents(
        chunks,
        embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
    )

    print(f"✅ Document ingestion complete. {len(chunks)} chunks saved.")


if __name__ == "__main__":
    DATA_PATH.mkdir(exist_ok=True)
    source_documents = load_documents()
    if source_documents:
        chunks = split_documents(source_documents)
        save_to_chroma(chunks)
    else:
        print("Ingestion failed: No documents found to process.")
