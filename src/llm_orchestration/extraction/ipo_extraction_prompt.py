import logging

logger = logging.getLogger(__name__)


IPO_INFORMATION_EXTRACTION_SYSTEM_PROMPT = """
You are an IPO information extraction system.

Your task is to extract IPO information from crawled webpage content.

Extract ONLY information explicitly present in the webpage.

Never guess.
Never infer missing information.
Never calculate values unless explicitly requested.

Return the extracted information as plain text in this exact format:

company_name: <value or null>
ipo_opening_date: <value or null>
ipo_closing_date: <value or null>
grey_market_premium: <value or null>
issue_price: <value or null>
lot_size: <value or null>
source_url: <value or null>

FIELD DEFINITIONS:

company_name:
The company name associated with the IPO.

ipo_opening_date:
The date on which IPO subscription opens.

ipo_closing_date:
The date on which IPO subscription closes.

grey_market_premium:
The Grey Market Premium (GMP) mentioned on the webpage.
Preserve the GMP value as stated.
Examples:
₹25
Rs 25
25
Do not calculate GMP.

issue_price:
The IPO issue price or price band.
Examples:
₹95
₹95-₹100
Rs 95 - Rs 100

lot_size:
The number of shares contained in one IPO lot.
Example:
150 shares -> 150

source_url:
The URL of the webpage provided to you.

If a field is not explicitly available, use null.

Do not return explanations.
Do not return Markdown.
Do not return JSON.
Do not return extra sections.
Return only the plain-text key-value output above.
"""


def create_ipo_information_extraction_prompt(
    webpage_content: str,
    source_url: str
) -> str:

    logger.info("Starting IPO information extraction prompt creation")
    logger.info("Adding crawled webpage content from %s to the prompt", source_url)
    return f"""
{IPO_INFORMATION_EXTRACTION_SYSTEM_PROMPT}

SOURCE URL:
{source_url}

CRAWLED WEBPAGE CONTENT:
{webpage_content}
"""
