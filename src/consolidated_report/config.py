import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.info("Loading consolidated_report configuration")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
logger.debug(f"Project root: {PROJECT_ROOT}")

SRC_ROOT = PROJECT_ROOT / "src"
LLM_ORCHESTRATION_ROOT = SRC_ROOT / "llm_orchestration"
logger.debug(f"Src root: {SRC_ROOT}")
logger.debug(f"LLM orchestration root: {LLM_ORCHESTRATION_ROOT}")

for path in (str(SRC_ROOT), str(LLM_ORCHESTRATION_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)
        logger.debug(f"Added to sys.path: {path}")

env_file = PROJECT_ROOT / ".env"
logger.info(f"Loading environment from: {env_file}")
load_dotenv(env_file)
logger.info("Environment variables loaded")

IPO_TEXT_FILE = SRC_ROOT / "llm_orchestration" / "output" / "ipo_information.txt"
PROMPT_YAML_FILE = Path(__file__).resolve().with_name("consolidation_prompt.yaml")
OUTPUT_MARKDOWN_FILE = Path(__file__).resolve().parent / "output" / "consolidated_ipo_report.md"
logger.debug(f"IPO text file: {IPO_TEXT_FILE}")
logger.debug(f"Prompt YAML file: {PROMPT_YAML_FILE}")
logger.debug(f"Output markdown file: {OUTPUT_MARKDOWN_FILE}")

OLLAMA_SERVER_URL = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME") or os.getenv("MODEL_NAME")
logger.info(f"Ollama server URL: {OLLAMA_SERVER_URL}")
logger.info(f"Model name: {MODEL_NAME}")
