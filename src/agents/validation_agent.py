from __future__ import annotations

import logging

from src.models.ipo_models import IPORecord, ValidationResult

logger = logging.getLogger(__name__)


class ValidationAgent:
    """Agent that checks whether extracted records are usable for consolidation."""

    def run(self, records: list[IPORecord]) -> ValidationResult:
        logger.info("Validation agent: validating %d records", len(records))

        issues: list[str] = []

        if not records:
            issues.append("No IPO records were extracted.")

        for record in records:
            if not record.company_name:
                issues.append("A record is missing company_name.")
            if not record.source_url:
                issues.append("A record is missing source_url.")

        unique_sources = {
            record.source_url
            for record in records
            if record.source_url
        }

        if records and not unique_sources:
            issues.append("No usable source URLs were retained.")

        result = ValidationResult(
            is_valid=not issues,
            issues=issues,
            records_ready_for_report=len(records),
        )

        logger.info(
            "Validation agent: valid=%s, issues=%d",
            result.is_valid,
            len(result.issues),
        )
        return result
