import logging

from ddgs import DDGS

from web_crawling.models import SearchResult

logger = logging.getLogger(__name__)


def search_web_for_pages(
    search_term: str,
    maximum_result_count: int = 10,
) -> list[str]:
    logger.info(
        "Starting web search for %r (up to %d results)",
        search_term,
        maximum_result_count,
    )

    page_urls = []

    with DDGS() as duckduckgo_client:
        logger.info("Submitting search request to DuckDuckGo")

        search_response_items = duckduckgo_client.text(
            search_term,
            max_results=maximum_result_count,
        )

        for result_position, search_response_item in enumerate(
            search_response_items,
            start=1,
        ):
            page_url = search_response_item.get("href", "")

            if not page_url:
                logger.warning(
                    "Skipping search result %d because it has no URL",
                    result_position,
                )
                continue

            logger.info(
                "Found search result %d: %s",
                result_position,
                page_url,
            )

            page_urls.append(page_url)

    logger.info(
        "Web search finished with %d URLs",
        len(page_urls),
    )

    return page_urls
