from __future__ import annotations

import logging

from ddgs import DDGS
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def search_web_for_ipo_pages(
    search_term: str,
    maximum_result_count: int = 5,
) -> list[str]:
    """Search the web and return URLs relevant to an IPO research question."""

    logger.info(
        "Research tool: searching web for %r with up to %d results",
        search_term,
        maximum_result_count,
    )

    page_urls: list[str] = []

    with DDGS() as duckduckgo_client:
        search_results = duckduckgo_client.text(
            search_term,
            max_results=maximum_result_count,
        )

        for result in search_results:
            page_url = result.get("href", "")
            if page_url and page_url not in page_urls:
                page_urls.append(page_url)

    logger.info("Research tool: found %d unique URLs", len(page_urls))
    return page_urls
