# IPO Oracle

IPO Oracle is a small research and extraction pipeline for gathering IPO-related information from web search results and crawled pages, then sending the content to a local Ollama model for extraction.

The project currently has three main components:

- Web research workflow: searches for relevant keywords, crawls pages, and saves the crawled content
- LLM orchestration workflow: loads the crawled data and extracts IPO details using a local Ollama model
- Streamlit frontend: interactive UI for research, extraction, and report generation

## Project structure

- `src/web_crawling/` — search, crawl, and save research results
- `src/llm_orchestration/` — extraction pipeline and output generation
- `src/consolidated_report/` — consolidated report generation from extracted data
- `src/streamlit_frontend/` — interactive web UI for the entire workflow
- `src/helper/` — shared utility functions
- `notebook/` — exploratory Jupyter notebooks for testing
- `requirements.txt` — Python dependencies

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

4. Confirm the model exists:

```bash
ollama pull iodose/nuextract-v1.5
```

5. Configure values in:

- `src/web_crawling/config.yaml`
- `src/llm_orchestration/config.yaml`

## Running the Application

### Option 1: Interactive Streamlit Frontend (Recommended)

The easiest way to use IPO Oracle is through the interactive Streamlit web interface:

```bash
python run_streamlit.py
```

Or directly:

```bash
streamlit run src/streamlit_frontend/app.py
```

The interface will open at `http://localhost:8501` and provides:
- **Research Tab**: Search and crawl IPO information from the web
- **Extraction Tab**: Process crawled content and extract IPO data
- **Report Tab**: Generate consolidated reports
- **Home Tab**: Workflow overview and status tracking

### Option 2: Command-line Scripts

Alternatively, run the workflows directly using Python scripts:

#### Research

```bash
python src/web_crawling/run_research.py
```

This searches the web for IPO-related pages, crawls the results, and writes JSON output to:

- `src/web_crawling/output/research_results.json`

#### Extraction

```bash
python src/llm_orchestration/main.py
```

This loads the crawled pages, sends them to Ollama for IPO extraction, and writes the raw plain-text output to:

- `src/llm_orchestration/output/ipo_information.txt`

#### Consolidated Report

```bash
python src/consolidated_report/main.py
```

This generates a consolidated IPO report from the extracted data and saves the markdown output to:

- `src/consolidated_report/output/consolidated_ipo_report.md`

## Notes

- The project currently saves raw LLM output as plain text instead of structured JSON or DataFrame output.
- The crawler and extraction logic depend on the repo path structure, so it is best to run commands from the project root or from the relevant script directory with the correct virtual environment activated.

## License

This project is for local research and experimentation purposes.
