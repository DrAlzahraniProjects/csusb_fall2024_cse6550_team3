import os
from roman import toRoman
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

def serve_pdf():
    """Used to open PDF file when a citation is clicked"""
    TEXTBOOK_PATH = os.path.join("data/default/textbook")
    file = st.query_params.get("file")

    # inference.py adjusts the pages for us
    # Ex: Chapter 1 at pg 34 in the PDF will have a page value of 34 here
    page = max(int(st.query_params.get("page", "1")), 1)
    adjusted_page = page - 33 # Chapter 1 will be assigned page 1 but we have to handle pages before it
    # For pages before Chapter 1
    if adjusted_page < 1: # For pages before Chapter 1
        # Display cover if first page else display roman numerals
        adjusted_page = "Cover" if (page - 1) == 0 else toRoman(page - 1) # Display cover if first page else display roman numerals

    if file:
        pdf_path = os.path.join(TEXTBOOK_PATH, file)
        if os.path.exists(pdf_path):
            with st.spinner(f"Loading page {adjusted_page} of the textbook..."):
                pdf_viewer(
                    pdf_path,
                    width=700,
                    height=1000,
                    pages_to_render=[page],
                    scroll_to_page=page,
                    render_text=True
                )
        else:
            st.error(f"PDF file not found at {pdf_path}")
    else:
        st.error("No PDF file specified in query parameters")