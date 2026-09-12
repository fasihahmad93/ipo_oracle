from __future__ import annotations

import logging

from src.telemetry import estimate_token_count
from src.tools.web_crawler_tool import crawl_ipo_pages
from src.tools.web_search_tool import search_web_for_ipo_pages

logger = logging.getLogger(__name__)


class ResearchAgent:
    """Agent responsible for finding and collecting IPO research evidence."""

    async def run(
        self,
        search_term: str,
        maximum_search_result_count: int,
    ) -> list[dict]:
        logger.info("Research agent: starting research for %r", search_term)

        urls = search_web_for_ipo_pages.invoke(
            {
                "search_term": search_term,
                "maximum_result_count": maximum_search_result_count,
            }
        )

        if not urls:
            logger.warning("Research agent: search returned no URLs")
            return []

        crawled_pages = await crawl_ipo_pages(urls)

        logger.info(
            "Research agent: completed with %d usable pages | "
            "total_scraped_estimated_tokens=%d",
            len(crawled_pages),
            sum(
                estimate_token_count(page.get("webpage_content", ""))
                for page in crawled_pages
            ),
        )
        return crawled_pages
