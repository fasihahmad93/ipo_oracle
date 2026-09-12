from __future__ import annotations

import logging

from langgraph.graph import END, START, StateGraph

from src.graph.nodes import (
    consolidation_node,
    extraction_node,
    orchestration_node,
    research_node,
    validation_node,
)
from src.graph.routing import route_after_orchestration, route_after_validation
from src.graph.state import IPOOracleState

logger = logging.getLogger(__name__)


def build_ipo_oracle_graph():
    """Build and compile the IPO Oracle LangGraph workflow."""

    logger.info("Building IPO Oracle LangGraph")

    workflow = StateGraph(IPOOracleState)

    workflow.add_node("research", research_node)
    workflow.add_node("extraction", extraction_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("orchestration", orchestration_node)
    workflow.add_node("consolidation", consolidation_node)

    workflow.add_edge(START, "research")
    workflow.add_edge("research", "extraction")
    workflow.add_edge("extraction", "validation")

    workflow.add_conditional_edges(
        "validation",
        route_after_validation,
        {
            "orchestration": "orchestration",
        },
    )

    workflow.add_conditional_edges(
        "orchestration",
        route_after_orchestration,
        {
            "research": "research",
            "extraction": "extraction",
            "consolidation": "consolidation",
            "stop": END,
        },
    )

    workflow.add_edge("consolidation", END)

    compiled_graph = workflow.compile()

    logger.info("IPO Oracle LangGraph compiled successfully")
    return compiled_graph
