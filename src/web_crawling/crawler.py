import logging

from crawl4ai import AsyncWebCrawler

from web_crawling.models import CrawledPage

logger = logging.getLogger(__name__)


import re


def remove_links_from_text(text: str) -> str:
    """
    Remove HTTP/HTTPS links from text.

    Args:
        text: Input text containing URLs.

    Returns:
        Text with URLs removed and whitespace cleaned.
    """
    url_pattern = r"https?://\S+|www\.\S+"

    text_without_links = re.sub(url_pattern, "", text)

    # Clean up extra whitespace left after removing URLs
    text_without_links = re.sub(r"\s+", " ", text_without_links).strip()

    return text_without_links



async def crawl_single_webpage(
    web_crawler: AsyncWebCrawler,
    target_url: str,
) -> CrawledPage:
    logger.info("Starting crawl for %s", target_url)
    try:
        logger.info("Sending crawl request for %s", target_url)
        crawl_response = await web_crawler.arun(url = target_url)

        if not crawl_response.success:
            logger.warning(
                "Crawl failed for %s: %s",
                target_url,
                crawl_response.error_message,
            )
            return CrawledPage(
                page_url=target_url,
                page_title=None,
                markdown_content="",
                was_crawled_successfully=False,
                error_message=crawl_response.error_message,
            )

        page_title = None

        if crawl_response.metadata:
            page_title = crawl_response.metadata.get("title")

        markdown_content = str(crawl_response.markdown or "")
        logger.info(
            "Extracted %d characters of markdown from %s",
            len(markdown_content),
            target_url,
        )
        logger.info("Crawl succeeded for %s", target_url)
        page =  CrawledPage(
            page_url=target_url,
            page_title=page_title,
            markdown_content=markdown_content,
            was_crawled_successfully=True,
        )
        page.markdown_content = remove_links_from_text(page.markdown_content)
        return page

    except Exception as crawl_error:

        logger.exception("Unexpected error while crawling %s", target_url)
        return CrawledPage(
            page_url=target_url,
            page_title=None,
            markdown_content="",
            was_crawled_successfully=False,
            error_message=str(crawl_error),
        )



async def crawl_multiple_webpages(
    target_urls: list[str],
) -> list[CrawledPage]:
    logger.info("Starting batch crawl for %d URLs", len(target_urls))
    crawled_page_records = []

    async with AsyncWebCrawler() as web_crawler:

        for url_position, target_url in enumerate(target_urls, start=1):
            logger.info("Crawling URL %d of %d", url_position, len(target_urls))

            crawled_page = await crawl_single_webpage(
                web_crawler,
                target_url,
            )

            crawled_page_records.append(crawled_page)

    logger.info("Batch crawl finished: %d pages processed", len(crawled_page_records))
    return crawled_page_records
