from __future__ import annotations

import logging

from src.config import get_int_env
from src.models.ipo_models import SupervisorDecision, ValidationResult

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """Deterministic supervisor that controls the workflow without an LLM."""

    def run(
        self,
        validation_result: ValidationResult,
        retry_count: int,
        record_count: int,
    ) -> SupervisorDecision:
        logger.info("Orchestrator agent: selecting deterministic next action")
        if validation_result.is_valid and record_count:
            decision = SupervisorDecision(
                next_action="consolidate",
                reason="Structured HTML extraction produced usable IPO records.",
            )
        elif retry_count < get_int_env("IPO_MAX_RESEARCH_RETRIES", 2):
            decision = SupervisorDecision(
                next_action="retry_research",
                reason="No usable IPO records were extracted; retrying with a broader query.",
            )
        else:
            decision = SupervisorDecision(
                next_action="stop",
                reason="No usable IPO records were extracted after the configured retries.",
            )

        logger.info(
            "Orchestrator agent: next_action=%s | reason=%s",
            decision.next_action,
            decision.reason,
        )
        return decision
