"""Responsive Streamlit interface for the IPO research pipeline."""

import asyncio
import logging
import os
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

logger = logging.getLogger(__name__)


def _load_search_defaults() -> tuple[str, int]:
    """Load initial search values from environment variables and YAML config."""
    config_path = PROJECT_ROOT / "src" / "web_crawling" / "config.yaml"
    with config_path.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file) or {}

    search_term = os.getenv("IPO_SEARCH_TERM", config.get("search_term", ""))
    result_count = int(
        os.getenv(
            "IPO_MAX_SEARCH_RESULTS",
            config.get("max_search_results", 5),
        )
    )
    return search_term, result_count


def _run_pipeline(search_term: str, maximum_search_result_count: int) -> pd.DataFrame:
    """Run the existing asynchronous research and report-generation pipeline."""
    from main import run_ipo_research_pipeline

    return asyncio.run(
        run_ipo_research_pipeline(
            search_term=search_term,
            maximum_search_result_count=maximum_search_result_count,
        )
    )


def _display_report(report: pd.DataFrame) -> None:
    """Render IPO records as readable cards and offer a CSV download."""
    st.subheader(f"{len(report)} IPO record(s)")

    if report.empty:
        st.info("No IPO records were returned. Try a broader search term.")
        return

    csv_data = report.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv_data,
        file_name="consolidated_ipo_report.csv",
        mime="text/csv",
        use_container_width=True,
    )

    for record in report.to_dict(orient="records"):
        company_name = record.get("company_name") or "Company not identified"
        with st.container(border=True):
            st.markdown(f"### {company_name}")
            for column, value in record.items():
                if column == "company_name":
                    continue
                display_value = (
                    str(value)
                    if value is not None and not pd.isna(value) and str(value).strip()
                    else "Not available"
                )
                st.text(f"{column.replace('_', ' ').title()}: {display_value}")

    with st.expander("View as a table"):
        st.dataframe(report, hide_index=True, use_container_width=True)


def main() -> None:
    """Render the mobile-friendly IPO Oracle interface."""
    st.set_page_config(
        page_title="IPO Oracle",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 960px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        @media (max-width: 600px) {
            .block-container {
                padding: 1rem 0.75rem 1.5rem;
            }
            h1 {
                font-size: 1.8rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("IPO Oracle")
    st.caption("Research Indian IPOs using web sources and your local Ollama model.")

    try:
        default_search_term, default_result_count = _load_search_defaults()
    except (OSError, ValueError, yaml.YAMLError) as error:
        logger.exception("Could not load the search defaults")
        st.error("Could not load the search settings.")
        with st.expander("Technical details"):
            st.exception(error)
        return

    with st.form("ipo_research_form"):
        search_term = st.text_input(
            "What should we search for?",
            value=default_search_term,
            placeholder="For example: IPO grey market premium India",
        )
        maximum_search_result_count = st.number_input(
            "Maximum search results",
            min_value=1,
            max_value=100,
            value=max(1, min(default_result_count, 100)),
            step=1,
        )
        submitted = st.form_submit_button(
            "Search and generate IPO report",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not search_term.strip():
            st.error("Enter a search term to start the research.")
        else:
            st.session_state.pop("ipo_report", None)
            try:
                with st.spinner(
                    "Searching the web, crawling pages, and generating the IPO report..."
                ):
                    st.session_state["ipo_report"] = _run_pipeline(
                        search_term.strip(),
                        int(maximum_search_result_count),
                    )
            except Exception as error:
                logger.exception("IPO research pipeline failed")
                st.error(
                    "The research pipeline failed. Check your internet connection, "
                    "DuckDuckGo availability, and local Ollama configuration."
                )
                with st.expander("Technical details"):
                    st.exception(error)

    report = st.session_state.get("ipo_report")
    if isinstance(report, pd.DataFrame):
        st.divider()
        st.subheader("Consolidated IPO report")
        _display_report(report)


if __name__ == "__main__":
    main()
