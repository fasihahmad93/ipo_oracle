from __future__ import annotations

import asyncio
import logging
import os

from src.config import get_int_env
from src.graph.ipo_oracle_graph import build_ipo_oracle_graph
from src.cli.banner import display_cli_banner

logger = logging.getLogger(__name__)


async def run_ipo_oracle(
    search_term: str | None = None,
    maximum_search_result_count: int | None = None,
) -> str:
    """Run the complete agentic IPO Oracle workflow."""

    search_term = search_term or os.getenv("IPO_SEARCH_TERM", "IPO GMP TODAY")
    maximum_search_result_count = maximum_search_result_count or get_int_env(
        "IPO_MAX_SEARCH_RESULTS", 5
    )
    logger.info("Starting IPO Oracle agentic workflow")

    graph = build_ipo_oracle_graph()

    initial_state = {
        "search_term": search_term,
        "maximum_search_result_count": maximum_search_result_count,
        "crawled_pages": [],
        "extracted_records": [],
        "retry_count": 0,
        "errors": [],
    }

    final_state = await graph.ainvoke(initial_state)

    final_report = final_state.get(
        "final_report",
        "IPO Oracle stopped before producing a final report.",
    )

    logger.info("IPO Oracle workflow completed")
    return final_report


def main() -> None:
    """CLI entry point."""

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    display_cli_banner()

    report = asyncio.run(
        run_ipo_oracle(
            search_term=os.getenv("IPO_SEARCH_TERM", "IPO GMP TODAY"),
            maximum_search_result_count=get_int_env("IPO_MAX_SEARCH_RESULTS", 5),
        )
    )

    print("\n" + "=" * 80)
    print("FINAL IPO REPORT")
    print("=" * 80 + "\n")
    print(report)


if __name__ == "__main__":
    main()
