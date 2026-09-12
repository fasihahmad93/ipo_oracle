# IPO Oracle

IPO Oracle researches Indian IPO grey-market-premium pages, parses their rendered HTML tables with pandas, and uses Ollama only to produce the final markdown report.

## Workflow

```text
Search → Crawl rendered HTML → Parse IPO/GMP tables → Validate → Final LLM report
```

```text
┌──────────────────┐
│ IPO search query │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ DDGS web search  │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Crawl4AI         │
│ rendered HTML    │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ pandas.read_html │
│ select IPO/GMP   │
│ tables           │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Normalize and    │
│ validate records │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Ollama           │
│ final Markdown   │
│ report only      │
└──────────────────┘
```

- Search uses DDGS.
- Crawl4AI provides rendered HTML and markdown.
- `pandas.read_html()` extracts table rows deterministically; no LLM extracts company data.
- The final report prompt lives in `src/prompts/final_report.yaml`.

## Setup

```bash
source .venv/bin/activate
pip install -r requirements.txt
ollama serve
```

Pull the model configured in `.env`, for example:

```bash
ollama pull qwen3.5:4b
```

## Configuration

All runtime settings are in `.env`:

```dotenv
OLLAMA_SERVER_URL=http://localhost:11434
OLLAMA_MODEL_NAME=qwen3.5:4b
OLLAMA_REQUEST_TIMEOUT_SECONDS=480
OLLAMA_TEMPERATURE=0
OLLAMA_REASONING=false
OLLAMA_CONTEXT_WINDOW=4096

IPO_SEARCH_TERM=IPO GMP TODAY
IPO_MAX_SEARCH_RESULTS=5
IPO_MAX_RESEARCH_RETRIES=2
```

## Run

```bash
python main.py
```

The logs show the tables selected from each source and the number of extracted records. Pages without standard HTML tables are skipped rather than being guessed by an LLM.

## Test

```bash
python -m pytest -q
```
