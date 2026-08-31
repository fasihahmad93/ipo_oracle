import logging

from .crawler_json_loader import CrawledWebpage
from .ipo_extraction_prompt import (
    create_ipo_information_extraction_prompt,
)
from .ollama_llm_client import OllamaLanguageModelClient

from src.llm_orchestration.configuration import MAX_WEBPAGE_CONTENT_LENGTH

logger = logging.getLogger(__name__)


class IPOInformationExtractor:

    def __init__(
        self,
        ollama_language_model_client: OllamaLanguageModelClient | None = None
    ):

        logger.info("Starting IPO information extractor initialization")
        self.ollama_language_model_client = (
            ollama_language_model_client
            or OllamaLanguageModelClient()
        )
        logger.info("IPO information extractor initialized")

    def extract_ipo_information_from_webpage(
        self,
        crawled_webpage: CrawledWebpage
    ) -> dict:

        logger.info("Starting IPO extraction for %s", crawled_webpage.source_url)
        logger.info("Creating the extraction prompt")
        webpage_content_for_extraction = crawled_webpage.webpage_content[
            :MAX_WEBPAGE_CONTENT_LENGTH
        ]
        logger.info(
            "Limiting webpage content from %d to %d characters for the model request",
            len(crawled_webpage.webpage_content),
            len(webpage_content_for_extraction),
        )
        ipo_information_extraction_prompt = (
            create_ipo_information_extraction_prompt(
                webpage_content=webpage_content_for_extraction,
                source_url=crawled_webpage.source_url,
            )
        )

        logger.info("Requesting plain-text IPO information from Ollama")
        raw_ipo_information = (
            self.ollama_language_model_client
            .generate_text(
                ipo_information_extraction_prompt
            )
        )
       
        logger.info("IPO extraction completed for %s", crawled_webpage.source_url)
        return raw_ipo_information

    def extract_ipo_information_from_webpages(
        self,
        crawled_webpages: list[CrawledWebpage]
    ) -> list[dict]:

        logger.info("Starting IPO extraction for %d crawled webpages", len(crawled_webpages))
        extracted_ipo_records = []

        for webpage_position, crawled_webpage in enumerate(crawled_webpages, start=1):

            try:
                logger.info("Large Language Model: %s ", self.ollama_language_model_client.ollama_model_name)
                logger.info(
                    "Extracting IPO information from webpage %d of %d: %s",
                    webpage_position,
                    len(crawled_webpages),
                    crawled_webpage.source_url,
                )
                extracted_ipo_information = (
                    self.extract_ipo_information_from_webpage(
                        crawled_webpage
                    )
                )

                extracted_ipo_records.append(
                    extracted_ipo_information
                )

                print(
                    f"Successfully extracted: "
                    f"{crawled_webpage.source_url}"
                )
                logger.info("IPO extraction succeeded for %s", crawled_webpage.source_url)

            except Exception as extraction_error:

                logger.exception("IPO extraction failed for %s", crawled_webpage.source_url)
                print(
                    f"Failed to extract: "
                    f"{crawled_webpage.source_url}"
                )

                print(
                    f"Error: {extraction_error}"
                )

        logger.info("Finished IPO extraction with %d records", len(extracted_ipo_records))
        return extracted_ipo_records
