from .config import MODEL_NAME, OLLAMA_SERVER_URL, OUTPUT_CSV_FILE, SCRAPPED_PAGES_DIRECTORY
from .report_generator import generate_consolidated_report, get_llm_client

__all__ = [
    "MODEL_NAME",
    "OLLAMA_SERVER_URL",
    "OUTPUT_CSV_FILE",
    "SCRAPPED_PAGES_DIRECTORY",
    "generate_consolidated_report",
    "get_llm_client",
]
