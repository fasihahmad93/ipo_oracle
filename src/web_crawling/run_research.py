import asyncio
import json
import logging
import re
import sys
from dataclasses import asdict
from pathlib import Path

import yaml

# Add src directory to path for absolute imports
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from web_crawling.research import search_and_crawl_webpages

logger = logging.getLogger(__name__)


def save_research_results_as_json(research_results: dict, 
                                  search_term: str,
                                  output_file_name: str = "research_results") -> Path:
    """Save research results as a JSON file and return its path."""

    logger.info("Starting JSON output creation")
    output_directory_path = Path(__file__).resolve().parent / "output"
    output_directory_path.mkdir(exist_ok=True)

    output_file_path = output_directory_path / (
        f"{output_file_name}.json"
    )
    serialized_research_results = {
        "crawled_pages": [
            asdict(crawled_page)
            for crawled_page in research_results["crawled_pages"]
        ],
    }

    logger.info("Writing results to %s", output_file_path)
    with output_file_path.open("w", encoding="utf-8") as output_json_file:
        json.dump(serialized_research_results, output_json_file, ensure_ascii=False, indent=2)

    logger.info("JSON output saved successfully")
    return output_file_path


def load_research_input_configuration(research_config_path: Path) -> dict:
    """Load and validate research inputs from a YAML configuration file."""

    logger.info("Loading research configuration from %s", research_config_path)
    with research_config_path.open(encoding="utf-8") as configuration_file:
        research_configuration = yaml.safe_load(configuration_file) or {}

    configured_search_term = research_configuration.get("search_term")
    configured_max_search_results = research_configuration.get("max_search_results")

    if not isinstance(configured_search_term, str) or not configured_search_term.strip():
        raise ValueError("'search_term' must be a non-empty string in the YAML config.")

    if (
        not isinstance(configured_max_search_results, int)
        or configured_max_search_results < 1
    ):
        raise ValueError("'max_search_results' must be a positive integer in the YAML config.")

    logger.info("Research configuration loaded successfully")
    return {
        "search_term": configured_search_term,
        "maximum_search_result_count": configured_max_search_results,
    }


async def run_research_workflow(
    search_term: str,
    maximum_search_result_count: int,
) -> Path:
    """Search, crawl, and save results for the supplied research inputs."""

    logger.info("Starting research workflow")

    logger.info("Researching search term: %s", search_term)

    research_results = await search_and_crawl_webpages(
        search_term=search_term,
        maximum_search_result_count=maximum_search_result_count,
    )

    logger.info(
        "Research complete: %d crawled pages",
        len(research_results["crawled_pages"]),
    )

    output_file_path = save_research_results_as_json(research_results, search_term)
    logger.info("Research output is available at %s", output_file_path)
    return output_file_path


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    research_configuration = load_research_input_configuration(
        Path(__file__).with_name("config.yaml")
    )
    asyncio.run(run_research_workflow(**research_configuration))
