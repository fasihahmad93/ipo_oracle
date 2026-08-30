import logging

from .crawler_json_loader import CrawledWebpage
from .ipo_extraction_prompt import (
    create_ipo_information_extraction_prompt,
)
from .ollama_llm_client import OllamaLanguageModelClient
from llm_orchestration.configuration import MAX_WEBPAGE_CONTENT_LENGTH

logger = logging.getLogger(__name__)


# def parse_plain_text_ipo_information(raw_ipo_information: str) -> dict[str, str | None]:
#     """Convert plain-text key/value output from Ollama into a dictionary."""
#     parsed_ipo_information: dict[str, str | None] = {}
#
#     for line in raw_ipo_information.splitlines():
#         line = line.strip()
#         if not line or ":" not in line:
#             continue
#
#         field_name, field_value = line.split(":", 1)
#         normalized_field_name = field_name.strip()
#         normalized_field_value = field_value.strip()
#
#         if normalized_field_value.lower() in {"null", "none"}:
#             parsed_ipo_information[normalized_field_name] = None
#         else:
#             parsed_ipo_information[normalized_field_name] = normalized_field_value
#
#     return parsed_ipo_information


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
        # extracted_ipo_information = parse_plain_text_ipo_information(raw_ipo_information)

        # logger.info("Validating the extracted IPO information")
        # validated_ipo_information = (
        #     validate_and_normalize_ipo_information(
        #         raw_ipo_information
        #     )
        # )

        # validated_ipo_information["source_url"] = (
        #     crawled_webpage.source_url
        # )

        # populated_ipo_fields = [
        #     field_name
        #     for field_name, field_value in validated_ipo_information.items()
        #     if field_name != "source_url" and field_value is not None
        # ]
        # logger.info(
        #     "IPO extraction returned %d populated fields: %s",
        #     len(populated_ipo_fields),
        #     ", ".join(populated_ipo_fields) or "none",
        # )
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
