from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class IPORecord(BaseModel):
    """Structured IPO information extracted from one source."""

    company_name: str | None = None
    ipo_opening_date: str | None = None
    ipo_closing_date: str | None = None
    grey_market_premium: str | None = None
    issue_price: str | None = None
    lot_size: str | None = None
    source_url: str | None = None


class ValidationResult(BaseModel):
    """Result produced by the validation agent."""

    is_valid: bool
    issues: list[str] = Field(default_factory=list)
    records_ready_for_report: int = 0


class SupervisorDecision(BaseModel):
    """Decision made by the orchestration agent."""

    next_action: Literal["retry_research", "re_extract", "consolidate", "stop"]
    reason: str
