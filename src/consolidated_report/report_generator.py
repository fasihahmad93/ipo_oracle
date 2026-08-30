from __future__ import annotations

import logging

from src.helper.file_import import import_text, import_yaml
from src.llm_orchestration.extraction.ollama_llm_client import OllamaLanguageModelClient

from .config import IPO_TEXT_FILE, MODEL_NAME, OLLAMA_SERVER_URL, OUTPUT_MARKDOWN_FILE, PROMPT_YAML_FILE

logger = logging.getLogger(__name__)


def get_llm_client() -> OllamaLanguageModelClient:
    logger.info("[get_llm_client] Starting LLM client initialization")
    
    if not MODEL_NAME:
        logger.error("[get_llm_client] MODEL_NAME or OLLAMA_MODEL_NAME not set in .env")
        raise ValueError("MODEL_NAME or OLLAMA_MODEL_NAME is not set in the .env file.")

    logger.debug(f"[get_llm_client] Creating Ollama client with model: {MODEL_NAME}")
    client = OllamaLanguageModelClient(
        ollama_server_url=OLLAMA_SERVER_URL,
        ollama_model_name=MODEL_NAME,
    )
    logger.info("[get_llm_client] LLM client initialized successfully")
    return client


def build_consolidation_prompt(ipo_text: str) -> str:
    logger.info("[build_consolidation_prompt] Starting prompt construction")
    logger.debug(f"[build_consolidation_prompt] IPO text length: {len(ipo_text)} characters")
    
    logger.debug(f"[build_consolidation_prompt] Loading prompt from: {PROMPT_YAML_FILE}")
    prompt_config = import_yaml(str(PROMPT_YAML_FILE))
    base_prompt = prompt_config.get("prompt", "")
    logger.debug(f"[build_consolidation_prompt] Base prompt loaded, length: {len(base_prompt)} characters")
    
    final_prompt = f"{base_prompt}\n\nIPO_INFORMATION_TEXT:\n{ipo_text}\n"
    logger.info(f"[build_consolidation_prompt] Prompt constructed successfully, total length: {len(final_prompt)} characters")
    return final_prompt


def generate_consolidated_report(
    ipo_text_file: str | object = IPO_TEXT_FILE,
    output_markdown_file: str | object = OUTPUT_MARKDOWN_FILE,
) -> str:
    logger.info("[generate_consolidated_report] Starting consolidated report generation")
    
    ipo_text_path = str(ipo_text_file)
    logger.debug(f"[generate_consolidated_report] IPO text file path: {ipo_text_path}")
    
    if not __import__("pathlib").Path(ipo_text_path).exists():
        logger.error(f"[generate_consolidated_report] IPO text file not found: {ipo_text_path}")
        raise FileNotFoundError(f"IPO text file not found: {ipo_text_path}")
    logger.info("[generate_consolidated_report] IPO text file found")

    logger.info("[generate_consolidated_report] Reading IPO text from file")
    ipo_text = import_text(ipo_text_path)
    logger.debug(f"[generate_consolidated_report] IPO text loaded, content length: {len(ipo_text)} characters")
    
    logger.info("[generate_consolidated_report] Building consolidation prompt")
    prompt = build_consolidation_prompt(ipo_text)
    logger.debug("[generate_consolidated_report] Prompt built successfully")
    
    logger.info("[generate_consolidated_report] Initializing LLM client")
    llm_client = get_llm_client()
    logger.debug("[generate_consolidated_report] LLM client ready")
    
    logger.info("[generate_consolidated_report] Sending text generation request to Ollama")
    report_markdown = llm_client.generate_text(prompt)
    logger.info(f"[generate_consolidated_report] LLM generation complete, output length: {len(report_markdown)} characters")

    output_path = __import__("pathlib").Path(output_markdown_file)
    logger.debug(f"[generate_consolidated_report] Output markdown file path: {output_path}")
    
    logger.info("[generate_consolidated_report] Creating output directory")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    logger.debug(f"[generate_consolidated_report] Output directory ready: {output_path.parent}")
    
    logger.info("[generate_consolidated_report] Writing consolidated report to file")
    output_path.write_text(report_markdown, encoding="utf-8")
    logger.info(f"[generate_consolidated_report] Report written successfully to: {output_path}")
    
    logger.info("[generate_consolidated_report] Consolidated report generation completed successfully")
    return report_markdown
