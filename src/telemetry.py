"""Small, dependency-free text and model-usage telemetry helpers."""

from __future__ import annotations

import logging
import re
from typing import Any


def estimate_token_count(text: str) -> int:
    """Return a tokenizer-independent token estimate for text not sent to Ollama.

    Ollama exposes exact counts for model requests.  Crawled text and the final
    rendered report have no canonical model tokenizer, so this count is clearly
    labelled as an estimate in logs.
    """

    return len(re.findall(r"\w+|[^\s\w]", text or ""))


def log_model_token_usage(
    logger: logging.Logger,
    operation: str,
    response: Any,
    output_text: str,
) -> None:
    """Log Ollama token counters plus a portable estimate of returned text."""

    metadata = getattr(response, "response_metadata", {}) or {}
    prompt_tokens = metadata.get("prompt_eval_count")
    generated_tokens = metadata.get("eval_count")
    total_tokens = (
        prompt_tokens + generated_tokens
        if isinstance(prompt_tokens, int) and isinstance(generated_tokens, int)
        else None
    )
    logger.info(
        "%s | model_prompt_tokens=%s | model_generated_tokens=%s | "
        "model_total_tokens=%s | output_estimated_tokens=%d",
        operation,
        prompt_tokens if prompt_tokens is not None else "unavailable",
        generated_tokens if generated_tokens is not None else "unavailable",
        total_tokens if total_tokens is not None else "unavailable",
        estimate_token_count(output_text),
    )
