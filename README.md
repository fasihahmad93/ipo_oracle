# IPO Oracle

IPO Oracle is a local IPO research tool for the Indian market. It searches the web for IPO/GMP pages, preserves their source HTML tables, and asks a local Ollama model to produce one filtered, consolidated IPO CSV.

It has two stages:

- Web research workflow: searches for relevant keywords, crawls pages, and saves the crawled content
- Consolidated-report workflow: combines every crawled HTML table into one IPO table using a local Ollama model

## Project structure

- `src/web_crawling/` — search, crawl, and save research results
- `src/consolidated_ipo_report/` — consolidated IPO table prompt, Ollama client, and report output
- `notebook/` — exploratory Jupyter notebooks for testing
- `requirements.txt` — Python dependencies

## Configuration

Create a `.env` file in the project root with the following values:

```dotenv
OLLAMA_SERVER_URL=http://localhost:11434
OLLAMA_MODEL_NAME=qwen2.5:3b
OLLAMA_REQUEST_TIMEOUT_SECONDS=480
OLLAMA_TEMPERATURE=0
OLLAMA_CONTEXT_WINDOW=32000

IPO_SEARCH_TERM=IPO GMP TODAY
IPO_MAX_SEARCH_RESULTS=3
IPO_HTML_SOURCE_DIRECTORY=src/web_crawling/scrapped pages
IPO_OUTPUT_CSV_FILE=src/consolidated_ipo_report/output/consolidated_ipo_report.csv
```

The model instructions are kept separately in `src/consolidated_ipo_report/consolidation_prompt.yaml`.

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure Ollama is running locally:

```bash
ollama serve
```

4. Pull the model configured as `OLLAMA_MODEL_NAME` in `.env` (for example):

```bash
ollama pull qwen2.5:3b
```

5. Configure the project using the `.env` example above.

## Run the research crawl

From the project root:

```bash
python src/web_crawling/run_research.py
```

This standalone step searches the web for IPO-related pages, crawls the results, and writes:

- `src/web_crawling/output/research_results.json`
- The original HTML for each successfully crawled page in `src/web_crawling/scrapped pages/`, preserving HTML tables. This folder is cleared at the start of each research workflow.

## Run the complete pipeline

From the project root:

```bash
python main.py
```

This searches and crawls webpages, sends all extracted HTML tables to Ollama in one request, and writes the consolidated table to:

- `src/consolidated_ipo_report/output/consolidated_ipo_report.csv`

The standalone crawl uses `src/web_crawling/config.yaml`; `main.py` uses the `.env` search values above.

## Output

The final CSV contains `company_name`, `price_band`, `lot_size`, `end_date_of_applying`, and `gmp`. Only IPOs that the source tables explicitly show as open are included.

## License

This project is for local research and experimentation purposes.
