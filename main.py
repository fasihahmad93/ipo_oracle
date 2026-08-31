import asyncio
import logging

from src.web_crawling.run_research import (
    run_research_workflow,
)

from src.llm_orchestration.run_llm_orchestration import (
    run_ipo_information_extraction_pipeline,
)

from src.consolidated_report.report_generator import (
    generate_consolidated_report,
)

from src.cli.banner import display_cli_banner


logger = logging.getLogger(__name__)


async def run_ipo_research_pipeline(
    search_term: str,
    maximum_search_result_count: int = 2,
) -> str:
    """
    Run the complete IPO research pipeline.

    Pipeline:
        1. Search and crawl relevant IPO webpages.
        2. Extract IPO information using the LLM.
        3. Consolidate the extracted information into a final report.

    Returns:
        The final consolidated IPO report as text.
    """

    logger.info(
        "Starting IPO research pipeline for search term: %r",
        search_term,
    )

    # ---------------------------------------------------------
    # Step 1: Web crawling
    # ---------------------------------------------------------

    logger.info(
        "Step 1/3: Starting web research"
    )

    research_output_file = await run_research_workflow(
        search_term=search_term,
        maximum_search_result_count=maximum_search_result_count,
    )

    logger.info(
        "Web research completed successfully: %s",
        research_output_file,
    )

    # ---------------------------------------------------------
    # Step 2: LLM extraction
    # ---------------------------------------------------------

    logger.info(
        "Step 2/3: Starting IPO information extraction"
    )

    ipo_information_text = (
        run_ipo_information_extraction_pipeline()
    )

    logger.info(
        "IPO information extraction completed"
    )

    # ---------------------------------------------------------
    # Step 3: Consolidation
    # ---------------------------------------------------------

    logger.info(
        "Step 3/3: Starting report consolidation"
    )

    final_ipo_report = generate_consolidated_report()

    logger.info(
        "IPO report consolidation completed"
    )

    logger.info(
        "IPO research pipeline completed successfully"
    )

    return final_ipo_report


def main() -> None:
    """
    Application entry point.
    """

    display_cli_banner()
    
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    search_term = "IPO GMP TODAY"

    final_ipo_report = asyncio.run(
        run_ipo_research_pipeline(
            search_term=search_term,
            maximum_search_result_count=3,
        )
    )

    print()
    print("=" * 80)
    print("FINAL IPO REPORT")
    print("=" * 80)
    print()
    print(final_ipo_report)


if __name__ == "__main__":
    main()