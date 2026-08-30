import asyncio
import logging

from web_crawling.run_research import load_research_input_configuration, run_research_workflow
from llm_orchestration.run_llm_orchestration import run_ipo_information_extraction_pipeline
from consolidated_report.run_generate_report import run_consolidated_report_generation_pipeline

logger = logging.getLogger(__name__)


async def run_ipo_research_pipeline(
    search_term: str,
    maximum_search_result_count: int = 5,
):
    """
    Run the complete IPO research pipeline.

    Pipeline:
        1. Search the web for relevant IPO GMP pages.
        2. Crawl the discovered webpages.
        3. Extract IPO information using the LLM.
        4. Consolidate the extracted information into a final report.
    """

    logger.info(
        "Starting IPO research pipeline for search term: %r",
        search_term,
    )

    # ---------------------------------------------------------
    # Step 1: Search for relevant webpages
    # ---------------------------------------------------------

    logger.info("Step 1/4: Searching the web")

    search_results = search_web_for_pages(
        search_term=search_term,
        maximum_result_count=maximum_search_result_count,
    )

    logger.info(
        "Found %d potentially relevant webpages",
        len(search_results),
    )

    if not search_results:
        logger.warning(
            "No webpages found for search term: %r",
            search_term,
        )
        return None

    # ---------------------------------------------------------
    # Step 2: Crawl webpages
    # ---------------------------------------------------------

    logger.info("Step 2/4: Crawling webpages")

    crawled_webpages = await crawl_webpages(
        search_results
    )

    logger.info(
        "Successfully crawled %d webpages",
        len(crawled_webpages),
    )

    if not crawled_webpages:
        logger.warning(
            "No webpages were successfully crawled"
        )
        return None

    # ---------------------------------------------------------
    # Step 3: Extract IPO information
    # ---------------------------------------------------------

    logger.info(
        "Step 3/4: Extracting IPO information"
    )

    extracted_ipo_records = []

    for webpage_number, crawled_webpage in enumerate(
        crawled_webpages,
        start=1,
    ):

        logger.info(
            "Extracting IPO information from webpage %d/%d: %s",
            webpage_number,
            len(crawled_webpages),
            crawled_webpage.url,
        )

        try:

            ipo_record = await extract_ipo_information(
                crawled_webpage
            )

            if ipo_record:
                extracted_ipo_records.append(
                    ipo_record
                )

        except Exception:
            logger.exception(
                "Failed to extract IPO information from %s",
                crawled_webpage.url,
            )

    logger.info(
        "Successfully extracted IPO information from %d webpages",
        len(extracted_ipo_records),
    )

    if not extracted_ipo_records:
        logger.warning(
            "No IPO information was extracted"
        )
        return None

    # ---------------------------------------------------------
    # Step 4: Consolidate information
    # ---------------------------------------------------------

    logger.info(
        "Step 4/4: Consolidating IPO information"
    )

    final_ipo_report = consolidate_ipo_information(
        extracted_ipo_records
    )

    logger.info(
        "IPO research pipeline completed successfully"
    )

    return final_ipo_report


def main():
    """
    Application entry point.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    search_term = "IPO GMP"

    final_ipo_report = asyncio.run(
        run_ipo_research_pipeline(
            search_term=search_term,
            maximum_search_result_count=5,
        )
    )

    if final_ipo_report is None:
        print("No IPO information found.")
        return

    print("\n")
    print(final_ipo_report)


if __name__ == "__main__":
    main()