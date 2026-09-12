from __future__ import annotations

import logging

from src.models.ipo_models import IPORecord
from src.tools.ipo_extraction_tool import extract_ipo_records_from_html

logger = logging.getLogger(__name__)


class ExtractionAgent:
    """Convert IPO/GMP HTML tables into structured records without an LLM."""

    def run(self, crawled_pages: list[dict]) -> list[IPORecord]:
        logger.info("Extraction agent: processing %d crawled pages", len(crawled_pages))
        records: list[IPORecord] = []

        for position, page in enumerate(crawled_pages, start=1):
            source_url = page.get("source_url", "")
            logger.info(
                "Extraction agent: page %d/%d | source=%s",
                position,
                len(crawled_pages),
                source_url,
            )
            try:
                page_records = extract_ipo_records_from_html(
                    source_url=source_url,
                    html_content=page.get("html_content", ""),
                )
            except Exception:
                logger.exception("Extraction agent: HTML extraction failed for %s", source_url)
                continue

            records.extend(page_records)
            logger.info(
                "Extraction agent: page completed | source=%s | records=%d",
                source_url,
                len(page_records),
            )

        logger.info("Extraction agent: produced %d IPO records", len(records))
        return records
