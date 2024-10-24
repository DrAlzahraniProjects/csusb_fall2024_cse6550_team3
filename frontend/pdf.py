import os
from roman import toRoman
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

# Custom page handling Software Engineering: A PRACTITIONER’S APPROACH
def serve_default_textbook(page):
    # inference.py adjusts the pages for us
    # Ex: Chapter 1 at pg 34 in the PDF will have a page value of 34 here
    adjusted_page = page - 33 # Chapter 1 will be assigned page 1 but we have to handle pages before it
    # For pages before Chapter 1
    if adjusted_page < 1: # For pages before Chapter 1
        # Display cover if first page else display roman numerals
        adjusted_page = "Cover" if (page - 1) == 0 else toRoman(page - 1) # Display cover if first page else display roman numerals
    return page, adjusted_page


def serve_pdf():
    """Used to open PDF file when a citation is clicked"""
    pdf_path = st.query_params.get("file")

    page = max(int(st.query_params.get("page", 1)), 1)
    adjusted_page = page
    if pdf_path.split("/")[-2] == "default": # "Software Engineering: A PRACTITIONER’S APPROACH"
        page, adjusted_page = serve_default_textbook(page)
        
    if pdf_path:
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