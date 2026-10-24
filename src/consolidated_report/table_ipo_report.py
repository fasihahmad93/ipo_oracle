"""Create the final IPO table directly from the HTML saved by web crawling."""

import json
import logging
from datetime import date
from io import StringIO
from pathlib import Path

import pandas as pd
import yaml

from .ollama_client import OllamaLanguageModelClient

logger = logging.getLogger(__name__)
PROMPT_YAML_FILE = Path(__file__).with_name("consolidation_prompt.yaml")

IPO_COLUMNS = ["company_name", "price_band", "lot_size", "end_date_of_applying", "gmp"]
IPO_RECORDS_JSON_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {column: {"type": ["string", "null"]} for column in IPO_COLUMNS},
        "required": IPO_COLUMNS,
        "additionalProperties": False,
    },
}


def extract_table_from_html(html_file: str | Path) -> list[pd.DataFrame]:
    """Read every table in one saved crawl HTML document."""
    html_path = Path(html_file)
    try:
        return pd.read_html(StringIO(html_path.read_text(encoding="utf-8")))
    except ValueError as error:
        if "No tables found" not in str(error):
            raise
        logger.info("No HTML tables found in %s", html_path)
        return []


def extract_tables_from_directory(directory: str | Path) -> list[pd.DataFrame]:
    """Extract all HTML tables in stable file and table order."""
    directory_path = Path(directory)
    if not directory_path.is_dir():
        raise NotADirectoryError(f"HTML source directory not found: {directory_path}")
    tables: list[pd.DataFrame] = []
    for html_file in sorted(directory_path.rglob("*.html")):
        tables.extend(extract_table_from_html(html_file))
    if not tables:
        raise ValueError("No extracted tables are available to send to the LLM.")
    logger.info("Extracted %d HTML table(s) from %s", len(tables), directory_path)
    return tables


def save_extracted_tables_to_yaml(
    tables: list[pd.DataFrame], output_file: str | Path
) -> Path:
    """Serialize extracted DataFrames as a YAML list of row mappings.

    Args:
        tables: DataFrames extracted from the crawled HTML pages.
        output_file: Destination YAML file path.

    Returns:
        The path written.
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_tables = [
        {
            "table_number": table_number,
            "rows": json.loads(table.to_json(orient="records", force_ascii=False)),
        }
        for table_number, table in enumerate(tables, start=1)
    ]
    with output_path.open("w", encoding="utf-8") as yaml_file:
        yaml.safe_dump(
            {"tables": yaml_tables},
            yaml_file,
            allow_unicode=True,
            sort_keys=False,
        )
    logger.info("Saved %d extracted table(s) to %s", len(tables), output_path)
    return output_path


def build_consolidated_ipo_prompt(
    tables: list[pd.DataFrame], today: date | None = None
) -> str:
    """Build the notebook's single-request, consolidated IPO prompt."""
    if not tables:
        raise ValueError("No extracted tables are available to send to the LLM.")
    source_tables = "\n\n".join(
        f"Table {number}:\n{table.to_markdown(index=False)}"
        for number, table in enumerate(tables, start=1)
    )
    today_date = (today or date.today()).isoformat()
    with PROMPT_YAML_FILE.open(encoding="utf-8") as prompt_file:
        prompt_config = yaml.safe_load(prompt_file) or {}
    prompt_template = prompt_config.get("prompt")
    if not isinstance(prompt_template, str) or not prompt_template.strip():
        raise ValueError("consolidation_prompt.yaml must define a non-empty 'prompt'.")
    return prompt_template.format(
        today_date=today_date,
        source_tables=source_tables,
    )


def parse_ipo_records(llm_response: str) -> list[dict[str, str | None]]:
    """Parse the model response and strictly validate the IPO record shape."""
    response_text = llm_response.strip()
    if response_text.startswith("```"):
        _, _, response_text = response_text.partition("\n")
        response_text, _, _ = response_text.rpartition("```")
    try:
        records = json.loads(response_text.strip())
    except json.JSONDecodeError as error:
        raise ValueError("The model response must be a valid JSON array of IPO records.") from error
    if not isinstance(records, list):
        raise ValueError("The model response must be a JSON array of IPO records.")
    for record in records:
        if not isinstance(record, dict) or set(record) != set(IPO_COLUMNS):
            raise ValueError("Each IPO record must contain exactly the expected IPO fields.")
        if any(value is not None and not isinstance(value, str) for value in record.values()):
            raise ValueError("Each IPO field must be a string or null.")
    return records


def generate_consolidated_ipo_dataframe(
    html_source_directory: str | Path,
    ollama_client: OllamaLanguageModelClient,
    extracted_tables_yaml_file: str | Path | None = None,
) -> pd.DataFrame:
    """Send all saved source tables to Ollama once and return the final table."""
    extracted_tables = extract_tables_from_directory(html_source_directory)
    if extracted_tables_yaml_file is not None:
        save_extracted_tables_to_yaml(extracted_tables, extracted_tables_yaml_file)
    prompt = build_consolidated_ipo_prompt(extracted_tables)
    response = ollama_client.generate_text(prompt, response_format=IPO_RECORDS_JSON_SCHEMA)
    return pd.DataFrame(parse_ipo_records(response), columns=IPO_COLUMNS)
