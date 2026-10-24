import asyncio
import logging

import pandas as pd

from src.web_crawling.run_research import (
    run_research_workflow,
)

from src.consolidated_ipo_report.report_generator import (
    generate_consolidated_report,
)
from src.consolidated_ipo_report.config import IPO_MAX_SEARCH_RESULTS, IPO_SEARCH_TERM

from src.cli.banner import display_cli_banner


logger = logging.getLogger(__name__)


async def run_ipo_research_pipeline(
    search_term: str,
    maximum_search_result_count: int,
) -> pd.DataFrame:
    """
    Run the complete IPO research pipeline.

    Pipeline:
        1. Search and crawl relevant IPO webpages.
        2. Extract one consolidated IPO table from all crawled HTML tables.

    Returns:
        The consolidated IPO DataFrame.
    """

    logger.info(
        "Starting IPO research pipeline for search term: %r",
        search_term,
    )

    # ---------------------------------------------------------
    # Step 1: Web crawling
    # ---------------------------------------------------------

    logger.info(
        "Step 1/2: Starting web research"
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
        "Step 2/2: Starting consolidated IPO report generation"
    )

    final_ipo_report = (
        generate_consolidated_report()
    )

    logger.info(
        "Consolidated IPO report generation completed"
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
        level=logging.WARNING,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    final_ipo_report = asyncio.run(
        run_ipo_research_pipeline(
            search_term=IPO_SEARCH_TERM,
            maximum_search_result_count=IPO_MAX_SEARCH_RESULTS,
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
