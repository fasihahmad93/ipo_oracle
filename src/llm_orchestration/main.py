import logging
from pathlib import Path

from extraction.crawler_json_loader import (
    load_crawled_webpages_from_json,
)

logger = logging.getLogger(__name__)

from extraction.ipo_information_extractor import (
    IPOInformationExtractor,
)

from ipo_table_formatter import (
    convert_ipo_records_to_text,
    save_ipo_records_to_text,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CRAWLER_OUTPUT_JSON_FILE = str(
    PROJECT_ROOT / "src" / "web_crawling" / "output" / "research_results.json"
)
IPO_OUTPUT_TXT_FILE = str(
    Path(__file__).resolve().parent / "output" / "ipo_information.txt"
)


def run_ipo_information_extraction_pipeline():

    logger.info("Starting IPO information extraction pipeline")
    print("Loading crawled webpages...")

    logger.info("Loading crawled webpage records from %s", CRAWLER_OUTPUT_JSON_FILE)
    crawled_webpages = (
        load_crawled_webpages_from_json(
            CRAWLER_OUTPUT_JSON_FILE
        )
    )

    print(
        f"Loaded {len(crawled_webpages)} crawled webpages."
    )
    logger.info("Loaded %d crawled webpage records", len(crawled_webpages))

    logger.info("Creating the IPO information extractor")
    ipo_information_extractor = (
        IPOInformationExtractor()
    )

    print("Extracting IPO information with Ollama...")

    logger.info("Sending crawled webpage content to Ollama for extraction")
    extracted_ipo_records = (
        ipo_information_extractor
        .extract_ipo_information_from_webpages(
            crawled_webpages
        )
    )

    print(
        f"Successfully extracted "
        f"{len(extracted_ipo_records)} IPO records."
    )
    logger.info("Extracted %d IPO records", len(extracted_ipo_records))

    logger.info("Formatting extracted IPO records as plain text")
    ipo_text_output = convert_ipo_records_to_text(
        extracted_ipo_records
    )

    logger.info("Saving extracted IPO records to %s", IPO_OUTPUT_TXT_FILE)
    save_ipo_records_to_text(
        extracted_ipo_records,
        IPO_OUTPUT_TXT_FILE,
    )

    print("\nIPO INFORMATION\n")
    print(ipo_text_output)

    logger.info("IPO information extraction pipeline completed")
    return ipo_text_output


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    run_ipo_information_extraction_pipeline()
