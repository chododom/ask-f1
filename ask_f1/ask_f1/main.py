from fastapi import FastAPI
from ask_f1.routes.chat_router import router
import langsmith
from contextlib import asynccontextmanager
from ask_f1.utils.logger import logger

# from backend.services.chroma_db import ChromaDBService
# import backend.services.chroma_db as chroma_db
# from backend import __version__
from ask_f1.config import CFG


langsmith_client = langsmith.Client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up...")

    yield
    # Shutdown actions
    logger.info("Shutting down...")


app = FastAPI(
    title="Chef in my pocket",
    description="",
    lifespan=lifespan,
)


app.include_router(router, prefix="/v1")
