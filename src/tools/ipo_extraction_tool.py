"""Deterministic extraction of IPO records from rendered HTML tables."""

from __future__ import annotations

from io import StringIO
import logging
import re

import pandas as pd

from src.models.ipo_models import IPORecord
from src.telemetry import estimate_token_count

logger = logging.getLogger(__name__)


def _normalise_header(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).casefold()).strip()


def _find_column(columns: list[object], aliases: tuple[str, ...]) -> object | None:
    for alias in aliases:
        for column in columns:
            if alias in _normalise_header(column):
                return column
    return None


def _cell_value(value: object) -> str | None:
    if pd.isna(value):
        return None
    cleaned_value = re.sub(r"\s+", " ", str(value)).strip()
    if not cleaned_value or cleaned_value.casefold() in {"-", "--", "n/a", "na", "none", "null"}:
        return None
    return cleaned_value


def _flatten_columns(table: pd.DataFrame) -> pd.DataFrame:
    result = table.copy()
    if isinstance(result.columns, pd.MultiIndex):
        result.columns = [
            " ".join(str(part) for part in column if str(part).casefold() != "nan")
            for column in result.columns
        ]
    return result


def extract_ipo_records_from_html(source_url: str, html_content: str) -> list[IPORecord]:
    """Parse IPO/GMP HTML tables without asking an LLM to extract data."""

    if not html_content.strip():
        logger.warning("HTML extraction: no HTML available for %s", source_url)
        return []

    try:
        tables = pd.read_html(StringIO(html_content))
    except (ValueError, ImportError) as exc:
        logger.warning("HTML extraction: no readable tables for %s: %s", source_url, exc)
        return []

    records: list[IPORecord] = []
    logger.info("HTML extraction: parsed %d tables from %s", len(tables), source_url)
    for table_position, raw_table in enumerate(tables, start=1):
        table = _flatten_columns(raw_table)
        columns = list(table.columns)
        company_column = _find_column(
            columns,
            ("company name", "ipo name", "issue name", "company", "name"),
        )
        gmp_column = _find_column(columns, ("grey market premium", "gmp", "grey market"))
        opening_column = _find_column(columns, ("opening date", "open date", "issue open", "opens"))
        closing_column = _find_column(columns, ("closing date", "close date", "issue close", "closes"))
        issue_price_column = _find_column(columns, ("issue price", "price band", "price"))
        lot_size_column = _find_column(columns, ("lot size", "lot"))
        detail_columns = [
            gmp_column,
            opening_column,
            closing_column,
            issue_price_column,
            lot_size_column,
        ]
        if company_column is None or not any(detail_columns):
            continue

        logger.info(
            "HTML extraction: using table=%d | rows=%d | columns=%s",
            table_position,
            len(table),
            [str(column) for column in columns],
        )
        for _, row in table.iterrows():
            company_name = _cell_value(row[company_column])
            if not company_name:
                continue
            records.append(
                IPORecord(
                    company_name=company_name,
                    ipo_opening_date=_cell_value(row[opening_column]) if opening_column else None,
                    ipo_closing_date=_cell_value(row[closing_column]) if closing_column else None,
                    grey_market_premium=_cell_value(row[gmp_column]) if gmp_column else None,
                    issue_price=_cell_value(row[issue_price_column]) if issue_price_column else None,
                    lot_size=_cell_value(row[lot_size_column]) if lot_size_column else None,
                    source_url=source_url,
                )
            )

    logger.info(
        "HTML extraction completed | url=%s | records=%d | records_estimated_tokens=%d",
        source_url,
        len(records),
        estimate_token_count("\n".join(record.model_dump_json() for record in records)),
    )
    return records
