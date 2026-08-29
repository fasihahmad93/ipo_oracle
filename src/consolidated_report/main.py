import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("[main] Starting consolidated_report entry point")

# Add src root to path for absolute imports
SRC_ROOT = Path(__file__).resolve().parents[1]
logger.debug(f"[main] Src root: {SRC_ROOT}")

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
    logger.debug("[main] Added src root to sys.path")

logger.info("[main] Importing generate_consolidated_report")
from consolidated_report.report_generator import generate_consolidated_report
logger.info("[main] Import successful")


if __name__ == "__main__":
    logger.info("[main] Calling generate_consolidated_report()")
    try:
        result = generate_consolidated_report()
        logger.info("[main] Report generation completed successfully")
        print(result)
    except Exception as e:
        logger.error(f"[main] Error during report generation: {e}", exc_info=True)
        raise
