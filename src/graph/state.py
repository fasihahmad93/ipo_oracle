from __future__ import annotations

from typing import TypedDict

from src.models.ipo_models import IPORecord, SupervisorDecision, ValidationResult


class IPOOracleState(TypedDict, total=False):
    search_term: str
    maximum_search_result_count: int

    crawled_pages: list[dict]
    extracted_records: list[IPORecord]

    validation_result: ValidationResult
    supervisor_decision: SupervisorDecision

    retry_count: int
    final_report: str
    errors: list[str]
