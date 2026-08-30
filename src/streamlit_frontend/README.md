# Streamlit Frontend for IPO Oracle

This directory contains the Streamlit web interface for the IPO Oracle application.

## Directory Structure

```
streamlit_frontend/
├── __init__.py              # Package initialization
├── app.py                   # Main application entry point
├── utils.py                 # Utility functions and UI helpers
└── components/
    ├── __init__.py          # Components package
    ├── research_page.py     # Web research and crawling interface
    ├── extraction_page.py   # IPO data extraction interface
    └── consolidation_page.py # Report generation interface
```

## Features

### 🏠 Home Tab
- Overview of the application
- Workflow guide
- Status tracking for each step

### 🔍 Research Tab
- Search for IPO information across the web
- Configure search parameters
- View and manage crawled results
- Cache management

### 🔬 Extraction Tab
- Process crawled content
- Configure extraction settings
- View extracted IPO data
- Download results in multiple formats

### 📋 Report Tab
- Generate consolidated reports
- Select output format (Markdown, HTML, PDF)
- View and download generated reports
- Display report metadata

## Running the Application

### Option 1: Using the launcher script
```bash
python run_streamlit.py
```

### Option 2: Direct Streamlit command
```bash
streamlit run src/streamlit_frontend/app.py
```

### Option 3: Using make (if available)
```bash
make streamlit
```

## Access

Once running, the application will be available at:
```
http://localhost:8501
```

## Configuration

The app loads configuration from:
- `.env` file for environment variables
- `src/llm_orchestration/config.yaml` for LLM settings
- Session state for temporary data

## Session State Management

The app uses Streamlit's session state to track:
- `research_results`: Cached research data
- `research_completed`: Research workflow status
- `extraction_completed`: Extraction workflow status
- `report_generated`: Report generation status
- `report_content`: Generated report content

## Logging

All operations are logged with:
- Function entry/exit points
- Process steps and their status
- Data sizes and transformations
- Error details with stack traces

View logs in the console where you run the Streamlit command.

## Module Organization

The frontend is organized into reusable components:

### `utils.py`
- Path setup for imports
- Streamlit page configuration
- UI message helpers
- Logging utilities

### `components/research_page.py`
- Web search interface
- Page crawling status
- Results preview and management

### `components/extraction_page.py`
- Extraction configuration
- Content input and processing
- Output formatting options
- Download management

### `components/consolidation_page.py`
- Report generation interface
- Format selection
- Report viewing and export
- Metadata display

## Workflow

The recommended workflow:
1. **Research**: Search for IPO information and crawl pages
2. **Extraction**: Process crawled content and extract IPO data
3. **Report**: Consolidate extracted data into a comprehensive report

Each step builds on the previous one and uses cached data.

## Development

To extend the application:

1. **Add a new page component**:
   ```python
   # src/streamlit_frontend/components/new_page.py
   def new_page():
       st.header("New Feature")
       # Add your UI here
   ```

2. **Register the component**:
   - Add to `components/__init__.py`
   - Add a tab in `app.py`

3. **Add utilities**:
   - Add helper functions to `utils.py`
   - Use logging for debugging

## Troubleshooting

### Port 8501 already in use
```bash
streamlit run src/streamlit_frontend/app.py --logger.level=debug --server.port 8502
```

### Import errors
Ensure you're running from the project root and the `.venv` is activated.

### Cache/Session issues
Clear browser cache or restart the Streamlit server.

## Dependencies

Core dependencies:
- `streamlit` - Web framework
- `python-dotenv` - Environment management
- `PyYAML` - Configuration
- `requests` - HTTP requests for Ollama

See `requirements.txt` for complete list.
