import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.extraction_agent import ExtractionAgent
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.validation_agent import ValidationAgent
from src.llm.ollama_client import create_ollama_chat_model
from src.models.ipo_models import IPORecord, ValidationResult
from src.prompts.loader import load_prompt_template
from src.tools.ipo_extraction_tool import extract_ipo_records_from_html
from src.telemetry import estimate_token_count


def test_create_ollama_chat_model_uses_json_format(monkeypatch):
    captured = {}

    class DummyChatOllama:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr("src.llm.ollama_client.ChatOllama", DummyChatOllama)

    create_ollama_chat_model()

    assert captured["format"] == "json"
    assert captured["reasoning"] is False


def test_estimate_token_count_counts_words_and_punctuation():
    assert estimate_token_count("IPO GMP: Rs. 25") == 6


def test_final_report_prompt_is_loaded_from_yaml():
    prompt = load_prompt_template("final_report")

    assert "{records_text}" in prompt


def test_html_table_extraction_normalizes_an_ipo_table():
    html = """
    <table><tr><th>Company Name</th><th>GMP</th><th>Price Band</th><th>Lot Size</th></tr>
    <tr><td>Example IPO</td><td>₹25</td><td>₹100-110</td><td>135</td></tr></table>
    <table><tr><th>City</th><th>Population</th></tr><tr><td>Delhi</td><td>1</td></tr></table>
    """

    records = extract_ipo_records_from_html("https://example.com", html)

    assert len(records) == 1
    assert records[0].company_name == "Example IPO"
    assert records[0].grey_market_premium == "₹25"
    assert records[0].issue_price == "₹100-110"
    assert records[0].source_url == "https://example.com"


def test_validation_agent_flags_missing_or_invalid_data():
    records = [IPORecord(company_name=None, source_url=None)]

    result = ValidationAgent().run(records)

    assert result.is_valid is False
    assert "company_name" in "\n".join(result.issues)
    assert "source_url" in "\n".join(result.issues)


def test_extraction_agent_keeps_valid_records_and_skips_failures(monkeypatch):
    def fake_extract(source_url, html_content):
        if source_url == "https://bad.example":
            raise ValueError("bad source")
        return [IPORecord(company_name="Example IPO", source_url=source_url)]

    monkeypatch.setattr("src.agents.extraction_agent.extract_ipo_records_from_html", fake_extract)

    records = ExtractionAgent().run(
        [
            {"source_url": "https://good.example", "html_content": "good"},
            {"source_url": "https://bad.example", "html_content": "bad"},
        ]
    )

    assert len(records) == 1
    assert records[0].company_name == "Example IPO"


def test_orchestrator_agent_parses_and_validates_decision(monkeypatch):
    decision = OrchestratorAgent().run(
        validation_result=ValidationResult(
            is_valid=True,
            issues=[],
            records_ready_for_report=1,
        ),
        retry_count=0,
        record_count=1,
    )

    assert decision.next_action == "consolidate"
    assert "Structured HTML extraction" in decision.reason
