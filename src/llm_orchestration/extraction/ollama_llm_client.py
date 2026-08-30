import logging

import requests

from llm_orchestration.configuration import (
    OLLAMA_MODEL_NAME,
    OLLAMA_REQUEST_TIMEOUT_SECONDS,
    OLLAMA_SERVER_URL,
)

logger = logging.getLogger(__name__)


class OllamaLanguageModelClient:

    def __init__(
        self,
        ollama_server_url: str = OLLAMA_SERVER_URL,
        ollama_model_name: str = OLLAMA_MODEL_NAME,
    ):

        logger.info("Starting Ollama language-model client initialization")
        self.ollama_server_url = ollama_server_url
        self.ollama_model_name = ollama_model_name
        logger.info(
            "Ollama language-model client initialized for model %s at %s",
            self.ollama_model_name,
            self.ollama_server_url,
        )

    def generate_text(
        self,
        language_model_prompt: str,
    ) -> str:

        logger.info("Starting text generation with the Ollama language model")
        ollama_generate_endpoint = (
            f"{self.ollama_server_url}/api/generate"
        )

        ollama_request_payload = {
            "model": self.ollama_model_name,
            "prompt": language_model_prompt,
            "stream": False,
        }

        logger.info("Sending text-generation request to %s", ollama_generate_endpoint)
        ollama_response = requests.post(
            ollama_generate_endpoint,
            json=ollama_request_payload,
            timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS,
        )

        ollama_response.raise_for_status()
        logger.info("Ollama text-generation request completed successfully")

        ollama_response_data = ollama_response.json()
        generated_language_model_response = ollama_response_data["response"]

        logger.info("Returning generated text from Ollama")
        return generated_language_model_response
