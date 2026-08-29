import logging
from typing import Any

logger = logging.getLogger(__name__)


EXPECTED_IPO_INFORMATION_FIELDS = [
    "company_name",
    "ipo_opening_date",
    "ipo_closing_date",
    "grey_market_premium",
    "issue_price",
    "lot_size",
    "source_url",
]


def validate_and_normalize_ipo_information(
    extracted_ipo_information: dict[str, Any]
) -> dict[str, Any]:

    logger.info("Starting IPO information validation and normalization")
    validated_ipo_information = {
        ipo_information_field: extracted_ipo_information.get(
            ipo_information_field
        )
        for ipo_information_field
        in EXPECTED_IPO_INFORMATION_FIELDS
    }

    validated_ipo_information["lot_size"] = (
        normalize_ipo_lot_size(
            validated_ipo_information["lot_size"]
        )
    )

    populated_field_count = sum(
        field_value is not None
        for field_value in validated_ipo_information.values()
    )
    logger.info(
        "Validated IPO information contains %d populated fields",
        populated_field_count,
    )
    logger.info("IPO information validation and normalization completed")
    return validated_ipo_information


def normalize_ipo_lot_size(
    ipo_lot_size: Any
) -> int | None:

    logger.info("Starting IPO lot-size normalization")
    if ipo_lot_size is None:
        logger.info("Lot size is missing; returning no normalized value")
        return None

    if isinstance(ipo_lot_size, int):
        logger.info("Lot size is already an integer")
        return ipo_lot_size

    try:

        normalized_lot_size = str(
            ipo_lot_size
        ).replace(",", "").strip()

        normalized_lot_size_value = int(normalized_lot_size)
        logger.info("Lot size normalized successfully")
        return normalized_lot_size_value

    except ValueError:

        logger.warning("Could not convert the supplied lot size into an integer")
        return None
