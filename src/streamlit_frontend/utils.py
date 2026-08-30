"""Utility functions for Streamlit frontend."""

import logging
import sys
from pathlib import Path

import streamlit as st

logger = logging.getLogger(__name__)


def setup_python_paths():
    """Add src directory to sys.path for imports."""
    src_root = Path(__file__).resolve().parents[1]
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))
    logger.debug(f"Python paths configured: {sys.path[:2]}")


def configure_streamlit_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="IPO Oracle",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Custom CSS for better styling
    st.markdown(
        """
        <style>
        .main {
            padding: 2rem;
        }
        .sidebar .sidebar-content {
            padding: 2rem 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logger.debug("Streamlit page configured")


def display_header():
    """Display application header."""
    st.title("📈 IPO Oracle")
    st.markdown(
        """
        A comprehensive tool for IPO research, extraction, and consolidation.
        """
    )


def display_sidebar_info():
    """Display information in the sidebar."""
    with st.sidebar:
        st.markdown("## About")
        st.markdown(
            """
            **IPO Oracle** helps you:
            - Search and crawl IPO websites
            - Extract IPO data using AI/LLM
            - Consolidate information from multiple sources
            - Generate comprehensive reports
            """
        )
        
        st.markdown("---")
        st.markdown("### Navigation")
        st.markdown(
            """
            Use the tabs above to navigate between different workflows.
            """
        )


def show_success_message(message: str):
    """Display a success message."""
    st.success(message)
    logger.info(f"Success: {message}")


def show_error_message(message: str):
    """Display an error message."""
    st.error(message)
    logger.error(f"Error: {message}")


def show_info_message(message: str):
    """Display an info message."""
    st.info(message)
    logger.info(f"Info: {message}")


def show_warning_message(message: str):
    """Display a warning message."""
    st.warning(message)
    logger.warning(f"Warning: {message}")
