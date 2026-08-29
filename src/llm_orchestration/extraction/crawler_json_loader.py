import json
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class CrawledWebpage:
    source_url: str
    webpage_title: str
    webpage_content: str


def load_crawled_webpages_from_json(
    crawler_output_file_path: str,
) -> list[CrawledWebpage]:

    crawler_output_file = Path(crawler_output_file_path)

    if not crawler_output_file.exists():
        raise FileNotFoundError(
            f"Crawler output file not found: {crawler_output_file_path}"
        )

    with crawler_output_file.open("r", encoding="utf-8") as file_object:
        crawler_output_data = json.load(file_object)

    if isinstance(crawler_output_data, dict):
        crawled_webpage_records = crawler_output_data.get("crawled_pages", [])

    elif isinstance(crawler_output_data, list):
        crawled_webpage_records = crawler_output_data

    else:
        raise ValueError(
            "Crawler JSON must contain a list of crawled webpage records."
        )

    crawled_webpages = []

    for webpage_record in crawled_webpage_records:

        if not isinstance(webpage_record, dict):
            continue

        if not webpage_record.get("was_crawled_successfully", True):
            continue

        source_url = (
            webpage_record.get("page_url")
            or webpage_record.get("url")
            or webpage_record.get("source_url")
            or ""
        )

        webpage_title = (
            webpage_record.get("page_title")
            or webpage_record.get("title")
            or ""
        )

        webpage_content = (
            webpage_record.get("markdown_content")
            or webpage_record.get("markdown")
            or webpage_record.get("content")
            or ""
        )

        if not webpage_content:
            continue

        crawled_webpages.append(
            CrawledWebpage(
                source_url=source_url,
                webpage_title=webpage_title,
                webpage_content=webpage_content,
            )
        )

    logger.info(
        "Loaded %d crawled webpages from %s",
        len(crawled_webpages),
        crawler_output_file,
    )

    return crawled_webpages