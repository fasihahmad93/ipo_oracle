from pathlib import Path

import yaml


_CONFIG_PATH = Path(__file__).with_name("config.yaml")

with _CONFIG_PATH.open("r", encoding="utf-8") as configuration_file:
    _CONFIG = yaml.safe_load(configuration_file) or {}

OLLAMA_SERVER_URL = _CONFIG.get("ollama_server_url", "http://localhost:11434")
OLLAMA_MODEL_NAME = _CONFIG.get("ollama_model_name", "llama3.2")
OLLAMA_REQUEST_TIMEOUT_SECONDS = int(
    _CONFIG.get("ollama_request_timeout_seconds", 120)
)
MAX_WEBPAGE_CONTENT_LENGTH = int(
    _CONFIG.get("max_webpage_content_length", 15000)
)
