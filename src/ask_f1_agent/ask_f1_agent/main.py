from contextlib import asynccontextmanager

import langsmith

from fastapi import FastAPI

import ask_f1_agent.services.chroma_db as chroma_db

from ask_f1_agent.config import CFG
from ask_f1_agent.routes.chat_router import router
from ask_f1_agent.services.f1_mcp import mcp_manager
from ask_f1_agent.utils.logger import logger
from ask_f1_agent.utils.utils import get_package_root

langsmith_client = langsmith.Client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up...")

    chroma_db.CHROMA_SERVICE_INSTANCE = chroma_db.ChromaDBService(
        persist_directory=get_package_root(CFG.package_name) / CFG.chroma_persistence_dir
    )

    await mcp_manager.connect()

    yield
    # Shutdown actions
    logger.info("Shutting down...")
    await mcp_manager.disconnect()


app = FastAPI(
    title="Chef in my pocket",
    description="",
    lifespan=lifespan,
)


app.include_router(router, prefix="/v1")
