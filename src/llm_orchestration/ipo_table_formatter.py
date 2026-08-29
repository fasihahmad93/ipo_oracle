import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def convert_ipo_records_to_text(
    extracted_ipo_records: list[str],
) -> str:
    """Join raw LLM output snippets into a single plain-text export."""
    logger.info("Starting IPO plain-text export")
    if not extracted_ipo_records:
        return "No IPO records extracted."

    plain_text_ipo_records = "\n\n".join(
        str(record).strip() for record in extracted_ipo_records if str(record).strip()
    )
    logger.info("IPO plain-text export completed")
    return plain_text_ipo_records


def save_ipo_records_to_text(
    extracted_ipo_records: list[str],
    output_text_file_path: str,
) -> None:
    """Write extracted IPO records to a plain-text file."""

    logger.info("Starting IPO record text export")
    output_path = Path(output_text_file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    text_content = convert_ipo_records_to_text(extracted_ipo_records)
    output_path.write_text(text_content, encoding="utf-8")
    logger.info("IPO record text export completed: %s", output_path)
