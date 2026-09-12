from __future__ import annotations

import logging
import os

from langchain_ollama import ChatOllama

from src.config import get_bool_env, get_float_env, get_int_env

logger = logging.getLogger(__name__)


def create_ollama_chat_model(json_output: bool = True) -> ChatOllama:
    """Create the LangChain Ollama chat model from environment settings."""

    server_url = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434").strip()
    model_name = os.getenv("OLLAMA_MODEL_NAME", "qwen3.5:4b").strip()
    timeout_seconds = get_int_env("OLLAMA_REQUEST_TIMEOUT_SECONDS", 480)
    temperature = get_float_env("OLLAMA_TEMPERATURE", 0)
    reasoning = get_bool_env("OLLAMA_REASONING", False)
    context_window = get_int_env("OLLAMA_CONTEXT_WINDOW", 4096)

    logger.info(
        "Initializing LangChain Ollama model: model=%s, base_url=%s, timeout=%ss, "
        "temperature=%s, reasoning=%s, context_window=%s",
        model_name,
        server_url,
        timeout_seconds,
        temperature,
        reasoning,
        context_window,
    )

    return ChatOllama(
        model=model_name,
        base_url=server_url,
        temperature=temperature,
        timeout=timeout_seconds,
        format="json" if json_output else None,
        reasoning=reasoning,
        num_ctx=context_window,
    )
