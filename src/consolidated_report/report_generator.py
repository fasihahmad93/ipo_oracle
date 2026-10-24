"""Generate the final IPO report directly from saved crawl HTML tables."""

import logging
from pathlib import Path

import pandas as pd

from .config import (
    MODEL_NAME,
    OLLAMA_CONTEXT_WINDOW,
    OLLAMA_REQUEST_TIMEOUT_SECONDS,
    OLLAMA_SERVER_URL,
    OLLAMA_TEMPERATURE,
    OUTPUT_CSV_FILE,
    SCRAPPED_PAGES_DIRECTORY,
)
from .ollama_client import OllamaLanguageModelClient
from .table_ipo_report import generate_consolidated_ipo_dataframe

logger = logging.getLogger(__name__)


def get_llm_client() -> OllamaLanguageModelClient:
    """Create the configured local Ollama client."""
    return OllamaLanguageModelClient(
        ollama_server_url=OLLAMA_SERVER_URL,
        ollama_model_name=MODEL_NAME,
        request_timeout_seconds=OLLAMA_REQUEST_TIMEOUT_SECONDS,
        temperature=OLLAMA_TEMPERATURE,
        context_window=OLLAMA_CONTEXT_WINDOW,
    )


def generate_consolidated_report(
    html_source_directory: str | Path = SCRAPPED_PAGES_DIRECTORY,
    output_csv_file: str | Path = OUTPUT_CSV_FILE,
    ollama_client: OllamaLanguageModelClient | None = None,
    output_yaml_file: str | Path | None = None,
) -> pd.DataFrame:
    """Create and save the IPO table and its extracted source tables.

    The extracted source tables are written beside the CSV by default, using
    the filename ``extracted_ipo_tables.yaml``.
    """
    logger.info("Generating consolidated IPO table from %s", html_source_directory)
    output_path = Path(output_csv_file)
    yaml_output_path = Path(output_yaml_file) if output_yaml_file else (
        output_path.with_name("extracted_ipo_tables.yaml")
    )
    dataframe = generate_consolidated_ipo_dataframe(
        html_source_directory,
        ollama_client or get_llm_client(),
        yaml_output_path,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)
    logger.info("Saved %d IPO record(s) to %s", len(dataframe), output_path)
    return dataframe
