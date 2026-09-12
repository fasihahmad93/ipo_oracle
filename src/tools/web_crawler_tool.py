from __future__ import annotations

import logging

from crawl4ai import AsyncWebCrawler
from langchain_core.tools import tool

from src.web_crawling.crawler import crawl_single_webpage

logger = logging.getLogger(__name__)


async def crawl_ipo_pages(target_urls: list[str]) -> list[dict]:
    """Crawl IPO webpages and return serializable page records."""

    logger.info("Crawler tool: crawling %d URLs", len(target_urls))
    crawled_pages: list[dict] = []

    async with AsyncWebCrawler() as web_crawler:
        for position, target_url in enumerate(target_urls, start=1):
            logger.info(
                "Crawler tool: processing URL %d/%d: %s",
                position,
                len(target_urls),
                target_url,
            )

            page = await crawl_single_webpage(web_crawler, target_url)

            if page.was_crawled_successfully and page.markdown_content:
                crawled_pages.append(
                    {
                        "source_url": page.page_url,
                        "webpage_title": page.page_title or "",
                        "webpage_content": page.markdown_content,
                        "html_content": page.html_content,
                    }
                )
            else:
                logger.warning("Crawler tool: failed to crawl %s", target_url)

    logger.info("Crawler tool: successfully crawled %d pages", len(crawled_pages))
    return crawled_pages


@tool
def crawl_ipo_pages_sync_placeholder(target_urls: list[str]) -> str:
    """Placeholder tool description for LangChain tool discovery.

    The graph calls the async crawler directly because Crawl4AI is asynchronous.
    """

    return f"Crawl {len(target_urls)} IPO pages using the async crawler."
