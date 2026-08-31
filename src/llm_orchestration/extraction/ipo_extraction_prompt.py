import logging

logger = logging.getLogger(__name__)


IPO_INFORMATION_EXTRACTION_SYSTEM_PROMPT = """
You extract IPO information from webpage content.

Use ONLY information explicitly present in the webpage.
Never guess, infer, or calculate.

Return ONLY these 7 lines:

company_name: <value or null>
ipo_opening_date: <value or null>
ipo_closing_date: <value or null>
grey_market_premium: <value or null>
issue_price: <value or null>
lot_size: <value or null>
source_url: <value or null>

Rules:
- company_name: IPO company name.
- ipo_opening_date: IPO subscription opening date.
- ipo_closing_date: IPO subscription closing date.
- grey_market_premium: GMP exactly as stated.
- issue_price: IPO issue price or price band exactly as stated.
- lot_size: number of shares in one lot.
- source_url: use the supplied source URL.
- Use null when the value is not explicitly available.
- Do not return anything if the webpage content is not related to IPO information.
- Do not explain anything.
"""

def create_ipo_information_extraction_prompt(
    webpage_content: str,
    source_url: str,
    extraction_prompt: str = IPO_INFORMATION_EXTRACTION_SYSTEM_PROMPT
) -> str:

    logger.info(
        "Starting IPO information extraction prompt creation"
    )

    return f"""

Instruction:
{extraction_prompt}
    
SOURCE URL:
{source_url}

WEBPAGE CONTENT:
{webpage_content}
"""
