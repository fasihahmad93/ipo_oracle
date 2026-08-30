"""Research and web crawling component."""

import asyncio
import json
import logging
from pathlib import Path

import streamlit as st

logger = logging.getLogger(__name__)


def research_page():
    """Display the research and web crawling interface."""
    st.header("🔍 Web Research")
    st.markdown("Search the web and crawl pages for IPO information.")
    
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., IPO 2026 upcoming companies",
            help="Enter keywords to search for IPO information",
        )
    
    with col2:
        max_results = st.number_input(
            "Max Results",
            min_value=1,
            max_value=50,
            value=10,
            help="Maximum number of search results to crawl",
        )
    
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    start_research = col1.button(
        "▶️ Start Research",
        use_container_width=True,
        type="primary",
    )
    
    view_results = col2.button(
        "📊 View Results",
        use_container_width=True,
    )
    
    clear_cache = col3.button(
        "🗑️ Clear Cache",
        use_container_width=True,
    )
    
    st.markdown("---")
    
    # Status and output section
    if start_research:
        if not search_query:
            st.error("Please enter a search query")
            logger.warning("Research attempted without search query")
        else:
            try:
                with st.spinner(f"🔍 Searching and crawling for: {search_query}"):
                    logger.info(f"Starting research for: {search_query}")
                    
                    # Import here to avoid circular imports
                    from web_crawling.research import search_and_crawl_webpages
                    from dataclasses import asdict
                    
                    logger.debug("Running search and crawl operation")
                    research_results = asyncio.run(
                        search_and_crawl_webpages(search_query, max_results)
                    )
                    
                    # Save results
                    output_dir = Path(__file__).resolve().parents[2] / "web_crawling" / "output"
                    output_dir.mkdir(parents=True, exist_ok=True)
                    output_file = output_dir / "research_results.json"
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(
                            {
                                "search_term": search_query,
                                "crawled_pages": [
                                    {
                                        "url": page.page_url,
                                        "title": page.page_title,
                                        "content": page.markdown_content[:500],  # Preview first 500 chars
                                    }
                                    for page in research_results["crawled_pages"]
                                ],
                            },
                            f,
                            ensure_ascii=False,
                            indent=2,
                        )
                    
                    st.session_state.research_results = research_results
                    st.session_state.research_completed = True
                    
                    st.success(f"✅ Research completed! Found {len(research_results['crawled_pages'])} pages")
                    logger.info(f"Research completed: {len(research_results['crawled_pages'])} pages found")
                    
            except Exception as e:
                st.error(f"Error during research: {str(e)}")
                logger.error(f"Research error: {e}", exc_info=True)
    
    if view_results or st.session_state.get("research_completed"):
        if "research_results" in st.session_state:
            st.subheader("📋 Research Results")
            
            results = st.session_state.research_results
            pages = results.get("crawled_pages", [])
            
            st.metric("Total Pages Crawled", len(pages))
            
            if pages:
                st.markdown("#### Crawled Pages:")
                for i, page in enumerate(pages, 1):
                    with st.expander(f"📄 {i}. {page.page_title or page.page_url}", expanded=False):
                        st.markdown(f"**URL:** {page.page_url}")
                        st.markdown(f"**Content Preview:**")
                        st.text_area(
                            f"Content {i}",
                            value=page.markdown_content[:1000],
                            height=200,
                            disabled=True,
                            label_visibility="collapsed",
                        )
    
    if clear_cache:
        st.session_state.pop("research_results", None)
        st.session_state.pop("research_completed", None)
        st.success("Cache cleared")
        logger.info("Research cache cleared")
