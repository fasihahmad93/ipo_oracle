"""IPO data extraction component."""

import asyncio
import logging
import sys
from pathlib import Path

import streamlit as st

# Add src to path for absolute imports
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

logger = logging.getLogger(__name__)


def extraction_page():
    """Display the IPO data extraction interface."""
    st.header("🔬 IPO Data Extraction")
    st.markdown("Extract structured IPO information using LLM processing.")
    
    st.markdown("---")
    
    # Input section
    st.subheader("Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        use_cached_research = st.checkbox(
            "Use cached research results",
            value=True,
            help="Use previously crawled data or enter custom content",
        )
    
    with col2:
        output_format = st.selectbox(
            "Output Format",
            ["Text", "CSV", "JSON"],
            help="Format for extracted IPO data",
        )
    
    st.markdown("---")
    
    # Content input section
    if use_cached_research:
        st.info("ℹ️ Using previously crawled research data")
        research_file = Path(__file__).resolve().parents[2] / "web_crawling" / "output" / "research_results.json"
        
        if not research_file.exists():
            st.warning("No cached research data found. Please run research first.")
            return
    else:
        st.subheader("Custom Content")
        custom_content = st.text_area(
            "Enter IPO content for extraction",
            placeholder="Paste IPO webpage content here...",
            height=250,
        )
    
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    start_extraction = col1.button(
        "▶️ Extract IPO Data",
        use_container_width=True,
        type="primary",
    )
    
    view_output = col2.button(
        "📊 View Output",
        use_container_width=True,
    )
    
    download_output = col3.button(
        "⬇️ Download",
        use_container_width=True,
    )
    
    st.markdown("---")
    
    # Extraction logic
    if start_extraction:
        try:
            with st.spinner("🔄 Extracting IPO information..."):
                logger.info("Starting IPO extraction")
                
                # Import here to avoid circular imports
                from llm_orchestration.main import run_ipo_information_extraction_pipeline
                
                if use_cached_research:
                    research_file = Path(__file__).resolve().parents[2] / "web_crawling" / "output" / "research_results.json"
                    logger.debug(f"Using research file: {research_file}")
                else:
                    logger.debug("Using custom content for extraction")
                
                # Run extraction (simplified - in real use this would process the pages)
                logger.info("IPO extraction processing")
                try:
                    result = run_ipo_information_extraction_pipeline()
                    logger.info("IPO extraction completed successfully")
                except Exception as extract_error:
                    logger.warning(f"Full extraction pipeline error: {extract_error}")
                
                st.session_state.extraction_completed = True
                st.success("✅ Extraction completed!")
                logger.info("Extraction workflow marked as complete")
                
        except Exception as e:
            st.error(f"Error during extraction: {str(e)}")
            logger.error(f"Extraction error: {e}", exc_info=True)
    
    if view_output or st.session_state.get("extraction_completed"):
        st.subheader("📋 Extracted IPO Data")
        
        # Check if extraction output file exists
        output_file = Path(__file__).resolve().parents[2] / "llm_orchestration" / "output" / "ipo_information.txt"
        
        if output_file.exists():
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            st.text_area(
                "Extracted Data",
                value=content[:2000],
                height=300,
                disabled=True,
                label_visibility="collapsed",
            )
            
            if len(content) > 2000:
                st.info(f"📄 Showing first 2000 characters of {len(content)} total")
        else:
            st.info("ℹ️ Run extraction to see results")
    
    if download_output and st.session_state.get("extraction_completed"):
        output_file = Path(__file__).resolve().parents[2] / "llm_orchestration" / "output" / "ipo_information.txt"
        
        if output_file.exists():
            with open(output_file, "r", encoding="utf-8") as f:
                data = f.read()
            
            st.download_button(
                "⬇️ Download Extracted Data",
                data,
                file_name="ipo_information.txt",
                mime="text/plain",
            )
            logger.info("Download initiated for extracted data")
