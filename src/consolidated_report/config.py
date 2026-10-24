import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.info("Loading consolidated_report configuration")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
logger.debug(f"Project root: {PROJECT_ROOT}")

SRC_ROOT = PROJECT_ROOT / "src"
logger.debug(f"Src root: {SRC_ROOT}")

env_file = PROJECT_ROOT / ".env"
logger.info(f"Loading environment from: {env_file}")
load_dotenv(env_file)
logger.info("Environment variables loaded")

def _required_environment_variable(name: str) -> str:
    value = os.getenv(name)
    if not value or not value.strip():
        raise ValueError(f"{name} must be set in .env.")
    return value.strip()


def _positive_integer_environment_variable(name: str) -> int:
    value = int(_required_environment_variable(name))
    if value < 1:
        raise ValueError(f"{name} must be a positive integer.")
    return value


def _project_path_environment_variable(name: str) -> Path:
    configured_path = Path(_required_environment_variable(name))
    return configured_path if configured_path.is_absolute() else PROJECT_ROOT / configured_path


OLLAMA_SERVER_URL = _required_environment_variable("OLLAMA_SERVER_URL")
MODEL_NAME = _required_environment_variable("OLLAMA_MODEL_NAME")
OLLAMA_REQUEST_TIMEOUT_SECONDS = _positive_integer_environment_variable(
    "OLLAMA_REQUEST_TIMEOUT_SECONDS"
)
OLLAMA_TEMPERATURE = float(_required_environment_variable("OLLAMA_TEMPERATURE"))
OLLAMA_CONTEXT_WINDOW = _positive_integer_environment_variable("OLLAMA_CONTEXT_WINDOW")
IPO_SEARCH_TERM = _required_environment_variable("IPO_SEARCH_TERM")
IPO_MAX_SEARCH_RESULTS = _positive_integer_environment_variable(
    "IPO_MAX_SEARCH_RESULTS"
)
SCRAPPED_PAGES_DIRECTORY = _project_path_environment_variable(
    "IPO_HTML_SOURCE_DIRECTORY"
)
OUTPUT_CSV_FILE = _project_path_environment_variable("IPO_OUTPUT_CSV_FILE")
logger.info(f"Ollama server URL: {OLLAMA_SERVER_URL}")
logger.info(f"Model name: {MODEL_NAME}")
