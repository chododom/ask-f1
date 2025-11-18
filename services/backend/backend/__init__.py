from backend.utils.utils import get_version
from backend.utils.logger import logger

__version__ = "tmp"  # get_version()
logger.info(f"Running version: {__version__}")
