from __future__ import annotations

import logging

from src.agents.extraction_agent import ExtractionAgent
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.research_agent import ResearchAgent
from src.agents.validation_agent import ValidationAgent
from src.graph.state import IPOOracleState
from src.llm.ollama_client import create_ollama_chat_model
from src.prompts.loader import load_prompt_template
from src.telemetry import estimate_token_count, log_model_token_usage
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

_research_agent = ResearchAgent()
_extraction_agent = ExtractionAgent()
_validation_agent = ValidationAgent()
_orchestrator_agent = OrchestratorAgent()


async def research_node(state: IPOOracleState) -> dict:
    """Research node: search the web and crawl evidence."""

    retry_count = state.get("retry_count", 0)
    search_term = state["search_term"]

    if retry_count:
        search_term = f"{search_term} latest current IPO GMP dates price lot size"

    logger.info("Graph node: RESEARCH | retry=%d | query=%r", retry_count, search_term)

    crawled_pages = await _research_agent.run(
        search_term=search_term,
        maximum_search_result_count=state.get(
            "maximum_search_result_count",
            5,
        ),
    )

    return {
        "crawled_pages": crawled_pages,
        "retry_count": retry_count + 1,
    }


def extraction_node(state: IPOOracleState) -> dict:
    """Extraction node: turn each crawled page into a structured record."""

    logger.info("Graph node: EXTRACTION")

    records = _extraction_agent.run(state.get("crawled_pages", []))

    return {"extracted_records": records}


def validation_node(state: IPOOracleState) -> dict:
    """Validation node: check whether extracted evidence is usable."""

    logger.info("Graph node: VALIDATION")

    result = _validation_agent.run(
        state.get("extracted_records", [])
    )

    return {"validation_result": result}


def orchestration_node(state: IPOOracleState) -> dict:
    """Supervisor node: let the orchestration agent choose the next step."""

    logger.info("Graph node: ORCHESTRATION")

    decision = _orchestrator_agent.run(
        validation_result=state["validation_result"],
        retry_count=state.get("retry_count", 0),
        record_count=len(state.get("extracted_records", [])),
    )

    return {"supervisor_decision": decision}


def consolidation_node(state: IPOOracleState) -> dict:
    """Consolidation node: create the final human-readable report."""

    logger.info("Graph node: CONSOLIDATION")

    records_text = "\n\n".join(
        record.model_dump_json()
        for record in state.get("extracted_records", [])
    )
    logger.info(
        "Consolidation telemetry | record_count=%d | input_estimated_tokens=%d",
        len(state.get("extracted_records", [])),
        estimate_token_count(records_text),
    )

    prompt = ChatPromptTemplate.from_template(load_prompt_template("final_report"))

    model = create_ollama_chat_model(json_output=False)
    response = (prompt | model).invoke({"records_text": records_text})

    final_report = (
        response.content
        if isinstance(response.content, str)
        else str(response.content)
    )
    log_model_token_usage(
        logger,
        "Consolidation model telemetry",
        response,
        final_report,
    )

    logger.info(
        "Graph node: CONSOLIDATION completed | report_characters=%d | "
        "report_estimated_tokens=%d",
        len(final_report),
        estimate_token_count(final_report),
    )

    return {"final_report": final_report}
