"""Consolidated report generation component."""

import logging
from pathlib import Path

import streamlit as st

logger = logging.getLogger(__name__)


def consolidation_page():
    """Display the report consolidation interface."""
    st.header("📋 Consolidated Report")
    st.markdown("Generate a comprehensive IPO report from extracted data.")
    
    st.markdown("---")
    
    # Configuration section
    st.subheader("Report Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_format = st.selectbox(
            "Report Format",
            ["Markdown", "PDF", "HTML"],
            help="Output format for the consolidated report",
        )
    
    with col2:
        include_summary = st.checkbox(
            "Include Summary",
            value=True,
            help="Add executive summary to report",
        )
    
    include_tables = st.checkbox(
        "Include Data Tables",
        value=True,
        help="Include detailed tables in report",
    )
    
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    generate_report = col1.button(
        "▶️ Generate Report",
        use_container_width=True,
        type="primary",
    )
    
    view_report = col2.button(
        "👁️ View Report",
        use_container_width=True,
    )
    
    download_report = col3.button(
        "⬇️ Download Report",
        use_container_width=True,
    )
    
    st.markdown("---")
    
    # Generate report logic
    if generate_report:
        try:
            with st.spinner("📝 Generating consolidated report..."):
                logger.info("Starting consolidated report generation")
                
                # Check if extraction output exists
                ipo_file = Path(__file__).resolve().parents[2] / "llm_orchestration" / "output" / "ipo_information.txt"
                
                if not ipo_file.exists():
                    st.error("IPO extraction data not found. Please run extraction first.")
                    logger.warning("IPO data file not found")
                    return
                
                # Import here to avoid circular imports
                from consolidated_report.report_generator import generate_consolidated_report
                
                logger.debug("Running consolidated report generation")
                report_content = generate_consolidated_report()
                
                st.session_state.report_content = report_content
                st.session_state.report_generated = True
                
                st.success("✅ Report generated successfully!")
                logger.info("Consolidated report generated successfully")
                
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            logger.error(f"Report generation error: {e}", exc_info=True)
    
    if view_report or st.session_state.get("report_generated"):
        report_file = Path(__file__).resolve().parents[2] / "consolidated_report" / "output" / "consolidated_ipo_report.md"
        
        if report_file.exists():
            with open(report_file, "r", encoding="utf-8") as f:
                report_content = f.read()
            
            st.subheader("📄 Generated Report")
            
            if report_format == "Markdown":
                st.markdown(report_content)
            elif report_format == "HTML":
                st.markdown(report_content)  # Streamlit renders markdown as HTML
            else:  # PDF
                st.info("PDF export requires additional dependencies")
            
            logger.info(f"Report displayed in {report_format} format")
        else:
            st.info("ℹ️ Generate a report first to view it here")
    
    if download_report:
        report_file = Path(__file__).resolve().parents[2] / "consolidated_report" / "output" / "consolidated_ipo_report.md"
        
        if report_file.exists():
            with open(report_file, "r", encoding="utf-8") as f:
                report_content = f.read()
            
            # Determine file extension based on format
            extensions = {
                "Markdown": ".md",
                "PDF": ".pdf",
                "HTML": ".html",
            }
            ext = extensions.get(report_format, ".md")
            
            st.download_button(
                f"⬇️ Download as {report_format}",
                report_content,
                file_name=f"consolidated_ipo_report{ext}",
                mime="text/plain" if ext == ".md" else "text/html",
            )
            logger.info(f"Report download initiated ({report_format})")
    
    # Report metadata section
    if st.session_state.get("report_generated"):
        st.markdown("---")
        st.subheader("📊 Report Metadata")
        
        col1, col2, col3 = st.columns(3)
        
        report_file = Path(__file__).resolve().parents[2] / "consolidated_report" / "output" / "consolidated_ipo_report.md"
        
        if report_file.exists():
            file_size = report_file.stat().st_size
            mod_time = report_file.stat().st_mtime
            
            from datetime import datetime
            
            with col1:
                st.metric("File Size", f"{file_size / 1024:.2f} KB")
            
            with col2:
                st.metric("Last Generated", datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M"))
            
            with col3:
                st.metric("Format", report_format)
