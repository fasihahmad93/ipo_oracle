import logging

from crawl4ai import AsyncWebCrawler

from web_crawling.crawler import crawl_single_webpage
from web_crawling.search import search_web_for_pages

logger = logging.getLogger(__name__)


async def search_and_crawl_webpages(
    search_term: str,
    maximum_search_result_count: int = 5,
) -> dict:

    logger.info("Starting research for %r", search_term)

    # Step 1: Search the web
    logger.info("Step 1 of 3: searching the web")

    crawlable_urls = search_web_for_pages(
        search_term,
        maximum_result_count=maximum_search_result_count,
    )

    logger.info(
        "Found %d crawlable URLs",
        len(crawlable_urls),
    )

    # Step 2: Crawl the URLs
    crawled_page_records = []

    logger.info(
        "Step 2 of 3: crawling %d URLs",
        len(crawlable_urls),
    )

    async with AsyncWebCrawler() as web_crawler:

        for url_position, crawlable_url in enumerate(
            crawlable_urls,
            start=1,
        ):
            logger.info(
                "Crawling result %d of %d: %s",
                url_position,
                len(crawlable_urls),
                crawlable_url,
            )

            crawled_page = await crawl_single_webpage(
                web_crawler,
                crawlable_url,
            )

            if crawled_page is not None:
                crawled_page_records.append(crawled_page)

                logger.info(
                    "Crawl result %d of %d completed successfully",
                    url_position,
                    len(crawlable_urls),
                )
            else:
                logger.warning(
                    "Crawl result %d of %d failed",
                    url_position,
                    len(crawlable_urls),
                )

    # Step 3: Prepare results
    logger.info("Step 3 of 3: preparing research results")

    research_results = {
        "crawled_pages": crawled_page_records,
    }

    logger.info("Research finished for %r", search_term)

    return research_results
