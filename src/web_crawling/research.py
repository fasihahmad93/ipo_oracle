import logging
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler

from src.web_crawling.crawler import crawl_single_webpage
from src.web_crawling.models import CrawledPage
from src.web_crawling.search import search_web_for_pages

logger = logging.getLogger(__name__)
SCRAPPED_PAGES_DIRECTORY = Path(__file__).resolve().parent / "scrapped pages"


def clear_scrapped_pages_directory() -> Path:
    """Create the scraped-pages directory and remove its previous contents."""

    SCRAPPED_PAGES_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for entry in SCRAPPED_PAGES_DIRECTORY.iterdir():
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()

    logger.info("Cleared scraped pages directory: %s", SCRAPPED_PAGES_DIRECTORY)
    return SCRAPPED_PAGES_DIRECTORY


def save_crawled_pages_as_html(
    crawled_pages: list[CrawledPage],
    output_directory_path: Path,
) -> list[Path]:
    """Render crawled Markdown pages as standalone HTML documents."""

    saved_paths = []
    for page_number, crawled_page in enumerate(crawled_pages, start=1):
        if not crawled_page.was_crawled_successfully or not crawled_page.html_content:
            logger.warning(
                "Skipping HTML save for %s because no successful source HTML is available",
                crawled_page.page_url,
            )
            continue

        page_label = crawled_page.page_title or urlparse(crawled_page.page_url).netloc
        filename_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", page_label).strip("-._")
        filename_stem = filename_stem[:80] or f"page-{page_number}"
        output_file_path = output_directory_path / f"{page_number:03d}-{filename_stem}.html"

        output_file_path.write_text(crawled_page.html_content, encoding="utf-8")
        saved_paths.append(output_file_path)
        logger.info("Saved crawled page as HTML: %s", output_file_path)

    return saved_paths


async def search_and_crawl_webpages(
    search_term: str,
    maximum_search_result_count: int = 5,
) -> dict:

    logger.info("Starting research for %r", search_term)
    scrapped_pages_directory = clear_scrapped_pages_directory()

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
    save_crawled_pages_as_html(
        crawled_page_records,
        scrapped_pages_directory,
    )

    logger.info("Research finished for %r", search_term)

    return research_results
