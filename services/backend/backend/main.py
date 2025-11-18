from fastapi import FastAPI
from backend.routes.routes import router
import langsmith
from contextlib import asynccontextmanager
from backend.utils.logger import logger
from backend.services.chroma_db import ChromaDBService
import backend.services.chroma_db as chroma_db
from backend import __version__
from backend.config.config import CFG
from backend.utils.utils import get_package_root
import backend.tools.f1_mcp as f1_mcp


langsmith_client = langsmith.Client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up...")

    # Initialize the global ChromaDB service instance in the chroma_db module
    chroma_db.CHROMA_SERVICE_INSTANCE = ChromaDBService(
        persist_directory=get_package_root(CFG.package_name)
        / CFG.chroma_persistence_dir
    )
    logger.info("ChromaDB Service initialized.")

    f1_mcp.MCP_TOOLS = await f1_mcp.fetch_mcp_tools()

    yield
    # Shutdown actions
    logger.info("Shutting down...")
    if getattr(chroma_db, "CHROMA_SERVICE_INSTANCE", None):
        chroma_db.CHROMA_SERVICE_INSTANCE.close()
        logger.info("ChromaDB Service persisted and closed.")


app = FastAPI(
    title="Ask-F1 Backend Service",
    description="Backend service for Ask-F1 application",
    version=__version__,
    lifespan=lifespan,
)


app.include_router(router)
