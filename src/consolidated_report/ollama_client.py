"""Minimal client for a local Ollama generation endpoint."""

import logging

import requests

logger = logging.getLogger(__name__)


class OllamaLanguageModelClient:
    """Send non-streaming generation requests to a configured Ollama server."""

    def __init__(
        self,
        ollama_server_url: str,
        ollama_model_name: str,
        request_timeout_seconds: int,
        temperature: float,
        context_window: int,
    ):
        self.ollama_server_url = ollama_server_url.rstrip("/")
        self.ollama_model_name = ollama_model_name
        self.request_timeout_seconds = request_timeout_seconds
        self.temperature = temperature
        self.context_window = context_window

    def generate_text(
        self,
        language_model_prompt: str,
        response_format: str | dict | None = None,
    ) -> str:
        """Generate text, optionally constraining the response with JSON schema."""
        if not language_model_prompt.strip():
            raise ValueError("The Ollama prompt must not be empty.")
        payload = {
            "model": self.ollama_model_name,
            "prompt": language_model_prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_ctx": self.context_window,
            },
        }
        if response_format is not None:
            payload["format"] = response_format
        endpoint = f"{self.ollama_server_url}/api/generate"
        response = requests.post(
            endpoint,
            json=payload,
            timeout=self.request_timeout_seconds,
        )
        response.raise_for_status()
        response_data = response.json()
        if not isinstance(response_data, dict) or not isinstance(response_data.get("response"), str):
            raise ValueError("Ollama response must contain a string 'response' field.")
        generated_text = response_data["response"]
        logger.info("Ollama generation completed successfully (%d response characters)", len(generated_text))
        return generated_text
