from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchResult:
    page_title: str
    page_url: str
    page_description: Optional[str] = None


@dataclass
class CrawledPage:
    page_url: str
    page_title: Optional[str]
    markdown_content: str
    was_crawled_successfully: bool
    error_message: Optional[str] = None
