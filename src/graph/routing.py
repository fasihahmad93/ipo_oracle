from __future__ import annotations

import logging

from src.graph.state import IPOOracleState

logger = logging.getLogger(__name__)


def route_after_orchestration(state: IPOOracleState) -> str:
    """Route the graph according to the supervisor's decision."""

    decision = state["supervisor_decision"].next_action
    logger.info("Graph router: supervisor selected %s", decision)

    if decision == "retry_research":
        return "research"

    if decision == "re_extract":
        return "extraction"

    if decision == "consolidate":
        return "consolidation"

    return "stop"


def route_after_validation(state: IPOOracleState) -> str:
    """Always hand validation to the supervisor agent."""

    return "orchestration"
